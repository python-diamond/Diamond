# coding=utf-8

"""
The CephCollector collects utilization info from the Ceph storage system.

Documentation for ceph perf counters:
http://ceph.com/docs/master/dev/perf_counters/

#### Dependencies

 * ceph [http://ceph.com/]

"""

try:
    import json
    json  # workaround for pyflakes issue #13
except ImportError:
    import simplejson as json

import glob
import os
import subprocess

import diamond.collector
import diamond.convertor

# Metric name/path separator
_PATH_SEP = "."

_NSEC_PER_SEC = 1000000000

# Performance metric data types
_PERFCOUNTER_NONE = 0
_PERFCOUNTER_TIME = 0x1
_PERFCOUNTER_U64 = 0x2
_PERFCOUNTER_LONGRUNAVG = 0x4
_PERFCOUNTER_COUNTER = 0x8

def flatten_dictionary(input, path=[]):
    """Produces iterator of pairs where the first value is the key path and
    the second value is the value associated with the key. For example::

      {'a': {'b': 10},
       'c': 20,
       }

    produces::

      [([a,b], 10), ([c], 20)]
    """
    for name, value in sorted(input.items()):
        path.append(name)
        if isinstance(value, dict):
            for result in flatten_dictionary(value, path):
                yield result
        else:
            yield (path[:], value)
        del path[-1]

def lookup_dict_path(d, path, extra=[]):
    """Lookup value in dictionary based on path + extra.

    For instance, [a,b,c] -> d[a][b][c]
    """
    element = None
    for component in path + extra:
        d = d[component]
        element = d
    return element

class CephCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(CephCollector, self).get_default_config_help()
        config_help.update({
            'socket_path': 'The location of the ceph monitoring sockets.'
                           ' Defaults to "/var/run/ceph"',
            'socket_prefix': 'The first part of all socket names.'
                             ' Defaults to "ceph-"',
            'socket_ext': 'Extension for socket filenames.'
                          ' Defaults to "asok"',
            'ceph_binary': 'Path to "ceph" executable. '
                           'Defaults to /usr/bin/ceph.',
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(CephCollector, self).get_default_config()
        config.update({
            'socket_path': '/var/run/ceph',
            'socket_prefix': 'ceph-',
            'socket_ext': 'asok',
            'ceph_binary': '/usr/bin/ceph',
        })
        return config

    def _get_socket_paths(self):
        """Return a sequence of paths to sockets for communicating
        with ceph daemons.
        """
        socket_pattern = os.path.join(self.config['socket_path'],
                                      (self.config['socket_prefix']
                                       + '*.' + self.config['socket_ext']))
        return glob.glob(socket_pattern)

    def _get_counter_prefix_from_socket_name(self, name):
        """Given the name of a UDS socket, return the prefix
        for counters coming from that source.
        """
        base = os.path.splitext(os.path.basename(name))[0]
        if base.startswith(self.config['socket_prefix']):
            base = base[len(self.config['socket_prefix']):]
        return 'ceph.' + base.replace(".", "-")

    def _popen_check_output(self, *popenargs):
        """
        Collect Popen output and check for errors.

        This is inspired by subprocess.check_output, added in Python 2.7. This
        method provides similar functionality but will work with Python 2.6.
        """
        process = subprocess.Popen(*popenargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, err = process.communicate()
        retcode = process.poll()
        if retcode:
            msg = "Command '%s' exited with non-zero status %d" % \
                    (popenargs[0], retcode)
            raise Exception(msg)
        return output, err

    def _get_admin_socket_json(self, name, args):
        """Return parsed JSON from Ceph daemon admin socket.

        Values are decoded into Python types automatically, except for
        floating point numbers. Currently, time is the only value logged with
        a floating point number format, but is not actually a fractional value
        as the format would imply. Floats are handled on a case-by-case basis.

        Args:
            name: path to admin socket
            args: arguments to pass to admin socket
        Returns:
            Parsed JSON as dictionary
        """
        bin = self.config['ceph_binary']
        cmd = [bin, '--admin-daemon', name] + args.split()
        json_str, err = self._popen_check_output(cmd)
        try:
            # do not decode floats; leave as input string
            return json.loads(json_str, parse_float=lambda v: v)
        except Exception:
            self.log.error('Could not parse JSON output from %s', name)
            self.log.error('  stderr: %s', err)
            self.log.error('  json_str_len: %d', len(json_str))
            raise

    def _get_perf_counters(self, name):
        """Return perf counters and schema from admin socket.

        Args:
            name: path to admin socket

        Returns:
            Tuple (counters, schema)
        """
        counters = self._get_admin_socket_json(name, "perf dump")
        schema = self._get_admin_socket_json(name, "perf schema")
        return counters, schema

    def _ceph_time_to_seconds(self, val):
        """Convert Ceph time format into seconds.

        Args:
            val: string in format "seconds.nanoseconds"

        Returns:
            Time in seconds as a floating point number.
        """
        sec, nsec = map(lambda v: long(v), val.split("."))
        return float(sec * _NSEC_PER_SEC + nsec) / float(_NSEC_PER_SEC)

    def _get_byte_metrics(self, name, metric_value):
        """Return list of metrics derived from byte units.

        Args:
            name: the name of the metric
            metric_value: the value of the metric in bytes

        Returns:
            List of (name, value) pairs for each unit.
        """
        assert name.endswith("bytes")
        result = []
        for unit in self.config['byte_unit']:
            new_value = diamond.convertor.binary.convert(
                    value = metric_value, oldUnit = 'byte', newUnit = unit)
            new_name = name.replace("bytes", unit)
            result.append((new_name, new_value))
        return result

    def _publish_longrunavg(self, counter_prefix, stats, path, type):
        """Publish a long-running average metric.

        A long-running metric has two components: 'avgcount' and 'sum'. We
        publish both the raw components, and a derived metric named
        <metric>.last_interval_avg that is the average since the last run of
        the collector.

        For a given long-running average metric with name <metric>, we publish
        the following derived metrics:

            <metric>.sum
            <metric>.count
            <metric>.last_interval_avg

        Args:
            counter_prefix: string prefixed to metric names
            stats: dictionary containing performance counters
            path: full path of the metric name (e.g. [osd, op_rw_rlat])
            type: the metric type taken from the schema
        """
        # name of <metric>
        base_name = _PATH_SEP.join(filter(None, [counter_prefix] + path))
        total_sum_name = "%s%s%s" % (base_name, _PATH_SEP, "sum")
        total_count_name = "%s%s%s" % (base_name, _PATH_SEP, "count")
        delta_sum_name = "%s%s%s" % (base_name, _PATH_SEP, "delta_sum")
        delta_count_name = "%s%s%s" % (base_name, _PATH_SEP, "delta_count")
        delta_avg_name = "%s%s%s" % (base_name, _PATH_SEP, "last_interval_avg")

        # lookup raw metric component values
        total_sum = lookup_dict_path(stats, path, ['sum'])
        total_count = lookup_dict_path(stats, path, ['avgcount'])

        # perform metric-specific type conversions
        if type & _PERFCOUNTER_TIME:
            total_sum = self._ceph_time_to_seconds(total_sum)

        # Calculate deltas since last time we queried admin socket. The
        # derivitive function records from the last invocation the
        # total_sum/total_count, and simply returns the difference.
        delta_sum = self.derivative(delta_sum_name, total_sum, time_delta=False)
        delta_count = self.derivative(delta_count_name, total_count, time_delta=False)

        # prune out idle metrics
        if total_count == 0:
            return

        # average in the last collection interval
        if delta_count == 0:
            delta_avg = 0
        else:
            delta_avg = float(delta_sum) / float(delta_count)

        # publish raw data
        self.publish_gauge(total_sum_name, total_sum)
        self.publish_gauge(total_count_name, total_count)

        # publish averages
        self.publish_gauge(delta_avg_name, delta_avg, 6)

    def _publish_stats(self, counter_prefix, stats, schema):
        """Publish a set of performance counters.

        Args:
            counter_prefix: string prefixed to metric names
            stats: dictionary containing performance counters
            schema: performance counter schema
        """
        for path, type in flatten_dictionary(schema):
            # remove 'type' component to get metric name
            assert path[-1] == 'type'
            del path[-1]

            if type & _PERFCOUNTER_LONGRUNAVG:
                self._publish_longrunavg(counter_prefix, stats, path, type)
            else:
                name = _PATH_SEP.join(filter(None, [counter_prefix] + path))
                value = lookup_dict_path(stats, path)

                if type & _PERFCOUNTER_TIME:
                    value = self._ceph_time_to_seconds(value)
                    self.publish_gauge(name, value, 6)

                elif type & _PERFCOUNTER_U64:
                    # create a list of values to log. we'll either log a list
                    # of derived metrics, or the single metric we began with.
                    if name.endswith("bytes"):
                        values = self._get_byte_metrics(name, value)
                    else:
                        values = [(name, value)]

                    for name, value in values:
                        if type & _PERFCOUNTER_COUNTER:
                            self.publish_counter(name, value, 2)
                        else:
                            self.publish_gauge(name, value, 2)
                else:
                    self.log.error("Unexpected metric type: %s/%d", name, type)

    def collect(self):
        """
        Collect stats
        """
        socket_paths = self._get_socket_paths()
        self.log.info('Checking %d Ceph socket paths...', len(socket_paths))
        for path in socket_paths:
            self.log.debug('checking %s', path)
            counter_prefix = self._get_counter_prefix_from_socket_name(path)
            try:
                stats, schema = self._get_perf_counters(path)
            except Exception:
                self.log.exception('Skipping due to error: %s', path) 
            self._publish_stats(counter_prefix, stats, schema)
        return
