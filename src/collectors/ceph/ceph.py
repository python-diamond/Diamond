# coding=utf-8

"""
The CephCollector collects utilization info from Ceph services.

Documentation for ceph perf counters:
http://ceph.com/docs/master/dev/perf_counters/

#### Dependencies

 * ceph [http://ceph.com/]

"""

import json  # No need for simplejson fallback b/c ceph py modules are >=2.6
import glob
import os
import subprocess
import re
import diamond.collector
import diamond.convertor
from diamond.collector import str_to_bool


# Metric name/path separator
_PATH_SEP = "."

_NSEC_PER_SEC = 1000000000

# Performance metric data types
_PERFCOUNTER_NONE = 0
_PERFCOUNTER_TIME = 0x1
_PERFCOUNTER_U64 = 0x2
_PERFCOUNTER_LONGRUNAVG = 0x4
_PERFCOUNTER_COUNTER = 0x8


def flatten_dictionary(input_dict, path=list()):
    """Produces iterator of pairs where the first value is the key path and
    the second value is the value associated with the key. For example::

      {'a': {'b': 10},
       'c': 20,
       }

    produces::

      [([a,b], 10), ([c], 20)]
    """
    for name, value in sorted(input_dict.items()):
        path.append(name)
        if isinstance(value, dict):
            for result in flatten_dictionary(value, path):
                yield result
        else:
            yield (path[:], value)
        del path[-1]


def lookup_dict_path(d, path, extra=list()):
    """Lookup value in dictionary based on path + extra.

    For instance, [a,b,c] -> d[a][b][c]
    """
    element = None
    for component in path + extra:
        d = d[component]
        element = d
    return element


class CalledProcessError(Exception):
    pass


def _popen_check_output(*popenargs):
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
        raise CalledProcessError(msg)
    return output, err


class AdminSocketError(Exception):
    def __init__(self, socket_name, command):
        self.socket_name = socket_name
        self.command = command

    def __str__(self):
        return "Admin socket error calling %s on socket %s" % (self.command, self.socket_name)


class MonError(Exception):
    def __init__(self, cluster_name, command):
        self.cluster_name = cluster_name
        self.command = command

    def __str__(self):
        return "Mon command error calling %s on cluster %s" % (self.command, self.cluster_name)


class GlobalName(str):
    pass


class CephCollector(diamond.collector.Collector):
    def __init__(self, config, handlers):
        super(CephCollector, self).__init__(config, handlers)
        self.config['short_names'] = str_to_bool(self.config['short_names'])
        self.config['service_stats_global'] = str_to_bool(self.config['service_stats_global'])
        self.config['perf_counters_enabled'] = str_to_bool(self.config['perf_counters_enabled'])

    def get_default_config_help(self):
        config_help = super(CephCollector, self).get_default_config_help()
        config_help.update({
            'socket_path': 'The location of the ceph monitoring sockets.'
                           ' Defaults to "/var/run/ceph"',
            'socket_ext': 'Extension for socket filenames.'
                          ' Defaults to "asok"',
            'ceph_binary': 'Path to "ceph" executable. '
                           'Defaults to /usr/bin/ceph.',
            'short_names': "If true, use cluster names instead of UUIDs"
                           "in metric paths.  Defaults to true.",
            'cluster_prefix': "Prefix for per-cluster metrics.  Defaults"
                           "to 'ceph.cluster'.",
            'service_stats_global': "If true, stats from osds and mons are"
                                    "stored under the cluster prefix (not by host).  If false, these"
                                    "stats are stored in per-host paths."
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(CephCollector, self).get_default_config()
        config.update({
            'socket_path': '/var/run/ceph',
            'socket_ext': 'asok',
            'ceph_binary': '/usr/bin/ceph',
            'short_names': True,
            'cluster_prefix': 'ceph.cluster',
            'service_stats_global': False,
            'perf_counters_enabled': True
        })
        return config

    def get_metric_path(self, name, instance=None):
        """
        This collector returns some cluster-wide statistics rather than
        server-specific statistics, so we override this to
        avoid diamond prefixing the hostname to our metrics.
        """
        if isinstance(name, GlobalName):
            return ".".join([self.config['cluster_prefix'], name])
        else:
            return super(CephCollector, self).get_metric_path(name, instance)

    def _get_socket_paths(self):
        """Return a sequence of paths to sockets for communicating
        with ceph daemons.
        """
        socket_pattern = os.path.join(self.config['socket_path'],
                                      ('*.' + self.config['socket_ext']))
        return glob.glob(socket_pattern)

    def _parse_socket_name(self, path):
        """Parse a socket name like /var/run/ceph/foo-osd.2.asok

        Return a 3 tuple of cluster name, service type, service id
        """
        return re.match("^(.*)-(.*)\.(.*).{0}$".format(self.config['socket_ext']),
                        os.path.basename(path)).groups()

    def _publish_longrunavg(self, counter_prefix, stats, path, stat_type):
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
            stat_type: the metric type taken from the schema
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
        if stat_type & _PERFCOUNTER_TIME:
            total_sum = self._ceph_time_to_seconds(total_sum)

        # Calculate deltas since last time we queried admin socket. The
        # derivitive function records from the last invocation the
        # total_sum/total_count, and simply returns the difference.
        delta_sum = self.derivative(delta_sum_name, total_sum, time_delta=False)
        delta_count = self.derivative(delta_count_name, total_count, time_delta=False)

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

    def _ceph_time_to_seconds(self, val):
        """Convert Ceph time format into seconds.  Older Ceph
           versions output times as a string, while newer
           versions output a float (which we pass through)

        :param val: string in format "seconds.nanoseconds" or
                    floating point number.

        Returns:
            Time in seconds as a floating point number.
        """
        if isinstance(val, basestring):
            sec, nsec = map(lambda v: long(v), val.split("."))
            return float(sec * _NSEC_PER_SEC + nsec) / float(_NSEC_PER_SEC)
        else:
            return val

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
                value=metric_value, oldUnit='byte', newUnit=unit)
            new_name = name.replace("bytes", unit)
            result.append((new_name, new_value))
        return result

    def _publish_stats(self, counter_prefix, stats, schema, global_name=False):
        """Publish a set of Ceph performance counters, including schema.

        :param counter_prefix: string prefixed to metric names
        :param stats: dictionary containing performance counters
        :param schema: performance counter schema
        """
        for path, stat_type in flatten_dictionary(schema):
            # remove 'stat_type' component to get metric name
            assert path[-1] == 'type'
            del path[-1]

            if stat_type & _PERFCOUNTER_LONGRUNAVG:
                self._publish_longrunavg(counter_prefix, stats, path, stat_type)
            else:
                name = _PATH_SEP.join(filter(None, [counter_prefix] + path))
                if global_name:
                    name = GlobalName(name)

                value = lookup_dict_path(stats, path)

                if stat_type & _PERFCOUNTER_TIME:
                    value = self._ceph_time_to_seconds(value)
                    self.publish_gauge(name, value, 6)

                elif stat_type & _PERFCOUNTER_U64:
                    # create a list of values to log. we'll either log a list
                    # of derived metrics, or the single metric we began with.
                    if name.endswith("bytes"):
                        values = self._get_byte_metrics(name, value)
                    else:
                        values = [(name, value)]

                    for name, value in values:
                        if stat_type & _PERFCOUNTER_COUNTER:
                            self.publish_counter(name, value, 2)
                        else:
                            self.publish_gauge(name, value, 2)
                else:
                    self.log.error("Unexpected metric stat_type: %s/%d", name, stat_type)

    def _cluster_id_prefix(self, cluster_name, fsid):
        # We'll either use the cluster name (human friendly but may not be unique)
        # or the UUID (robust but obscure)
        if self.config['short_names']:
            return cluster_name
        else:
            return fsid

    def _publish_cluster_stats(self, cluster_name, fsid, prefix, stats, counter=False):
        """
        Given a stats dictionary, publish under the cluster path (respecting
        short_names and cluster_prefix)
        """


        for stat_name, stat_value in flatten_dictionary(
            stats,
            path=[self._cluster_id_prefix(cluster_name, fsid), prefix]
        ):
            name = GlobalName(stat_name)
            if counter:
                self.publish_counter(name, stat_value)
            else:
                self.publish_gauge(name, stat_value)

    def _admin_command(self, socket_path, command):
        try:
            json_blob, err = _popen_check_output(
                [self.config['ceph_binary'], '--admin-daemon', socket_path] + command)
        except subprocess.CalledProcessError:
            self.log.exception('Error calling to %s' % socket_path)
            raise AdminSocketError(socket_path, command)

        try:
            return json.loads(json_blob)
        except (ValueError, IndexError):
            self.log.exception('Error parsing output from %s' % socket_path)
            raise AdminSocketError(socket_path, command)

    def _mon_command(self, cluster, command):
        try:
            json_blob, err = _popen_check_output(
                [self.config['ceph_binary'], '--cluster', cluster, '-f', 'json-pretty'] + command)
        except subprocess.CalledProcessError:
            raise MonError(cluster, command)

        try:
            return json.loads(json_blob)
        except (ValueError, IndexError):
            self.log.exception('Error parsing output from %s: %s' % (cluster, command))
            raise MonError(cluster, command)

    def _collect_cluster_stats(self, path):
        """
        If this service is a mon and it is the leader of a quorum, then
        publish statistics about the cluster.
        """
        cluster_name, service_type, service_id = self._parse_socket_name(path)
        if service_type != 'mon':
            return

        # We have a mon, see if it is the leader
        mon_status = self._admin_command(path, ['mon_status'])
        if mon_status['state'] != 'leader':
            return
        fsid = mon_status['monmap']['fsid']

        # We are the leader, gather cluster-wide statistics
        self.log.debug("mon leader found, gathering cluster stats for cluster '%s'" % cluster_name)

        def publish_pool_stats(pool_id, stats):
            # Some of these guys we treat as counters, some as gauges
            delta_fields = ['num_read', 'num_read_kb', 'num_write', 'num_write_kb', 'num_objects_recovered',
                            'num_bytes_recovered', 'num_keys_recovered']
            for k, v in stats.items():
                self._publish_cluster_stats(cluster_name, fsid, "pool.{0}".format(pool_id), {k: v},
                                            counter=k in delta_fields)

        # Gather "ceph pg dump pools" and file the stats by pool
        for pool in self._mon_command(cluster_name, ['pg', 'dump', 'pools']):
            publish_pool_stats(pool['poolid'], pool['stat_sum'])

        all_pools_stats = self._mon_command(cluster_name, ['pg', 'dump', 'summary'])['pg_stats_sum']['stat_sum']
        publish_pool_stats('all', all_pools_stats)

        # Gather "ceph df"
        df = self._mon_command(cluster_name, ['df'])
        self._publish_cluster_stats(cluster_name, fsid, "df", df['stats'])

    def _get_perf_counters(self, name):
        """Return perf counters and schema from admin socket.

        Args:
            name: path to admin socket

        Returns:
            Tuple (counters, schema)
        """
        counters = self._admin_command(name, ['perf', 'dump'])
        schema = self._admin_command(name, ['perf', 'schema'])
        return counters, schema

    def _collect_service_stats(self, path):
        if not self.config['perf_counters_enabled']:
            return

        cluster_name, service_type, service_id = self._parse_socket_name(path)
        fsid = self._admin_command(path, ['config', 'get', 'fsid'])['fsid']

        stats, schema = self._get_perf_counters(path)
        if self.config['service_stats_global']:
            counter_prefix = "{0}.{1}.{2}".format(self._cluster_id_prefix(cluster_name, fsid), service_type, service_id)
            self._publish_stats(cluster_name, fsid, counter_prefix, stats, global_name=True)
        else:
            # The prefix is <cluster name>.<service type>.<service id>
            counter_prefix = "{0}.{1}.{2}".format(cluster_name, service_type, service_id)
            self._publish_stats(counter_prefix, stats, schema)

    def collect(self):
        """
        Collect stats
        """
        for path in self._get_socket_paths():
            self.log.debug('gathering service stats for %s', path)

            self._collect_service_stats(path)
            self._collect_cluster_stats(path)
