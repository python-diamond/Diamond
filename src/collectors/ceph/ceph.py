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


def flatten_dictionary(input_dict, path=None):
    """Produces iterator of pairs where the first value is the key path and
    the second value is the value associated with the key. For example::

      {'a': {'b': 10},
       'c': 20,
       }

    produces::

      [([a,b], 10), ([c], 20)]
    """
    if path is None:
        path = []

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
    process = subprocess.Popen(*popenargs,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
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
        message = "Admin socket error calling %s on socket %s"
        return message % (self.command, self.socket_name)


class MonError(Exception):
    def __init__(self, cluster_name, command):
        self.cluster_name = cluster_name
        self.command = command

    def __str__(self):
        message = "Mon command error calling %s on cluster %s"
        return message % (self.command, self.cluster_name)


class GlobalName(str):
    pass


class LocalName(str):
    pass


class CephCollector(diamond.collector.Collector):
    def __init__(self, config=None, handlers=[], name=None, configfile=None):
        super(CephCollector, self).__init__(config, handlers, name, configfile)
        for key in ('short_names',
                    'service_stats_global',
                    'perf_counters_enabled',
                    'osd_stats_enabled',
                    'long_running_detail'):
            self.config[key] = str_to_bool(self.config[key])

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
            'osd_stats_enabled': "Whether to enable OSD service stats.  These"
                           "are the most numerous and may overload"
                           "underpowered graphite instances when there are "
                           " 100s of OSDs. Defaults to true",
            'service_stats_global': "If true, stats from osds and mons are"
                                    "stored under the cluster prefix (not by"
                                    "host).  If false, these"
                                    "stats are stored in per-host paths.",
            'long_running_detail': "Whether to break down long running"
                                   "averages into sum/count/average (true), or"
                                   "only output the average from the last"
                                   "measurement interval (false).  Defaults"
                                   "to false."
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
            'osd_stats_enabled': True,
            'long_running_detail': False,
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
        elif isinstance(name, LocalName):
            return super(CephCollector, self).get_metric_path(name, instance)
        else:
            # explicit local or global indication to catch bugs more easily
            message = "Name '{0}' not LocalName or GlobalName".format(name)
            raise RuntimeError(message)

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
        pattern = "^(.*)-(.*)\.(.*).{0}$".format(self.config['socket_ext'])
        return re.match(pattern, os.path.basename(path)).groups()

    def _publish_longrunavg(self,
                            counter_prefix,
                            stats,
                            path,
                            stat_type,
                            name_class):
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
        def _make_stat_name(stat_name):
            parts = [counter_prefix] + path + [stat_name]
            clean_parts = filter(None, parts)
            return name_class(_PATH_SEP.join(clean_parts))

        total_sum_name = _make_stat_name("sum")
        total_count_name = _make_stat_name("count")
        delta_sum_name = _make_stat_name("delta_sum")
        delta_count_name = _make_stat_name("delta_count")
        delta_avg_name = _make_stat_name("last_interval_avg")

        # lookup raw metric component values
        total_sum = lookup_dict_path(stats, path, ['sum'])
        total_count = lookup_dict_path(stats, path, ['avgcount'])

        # perform metric-specific type conversions
        if stat_type & _PERFCOUNTER_TIME:
            total_sum = self._ceph_time_to_seconds(total_sum)

        # Calculate deltas since last time we queried admin socket. The
        # derivitive function records from the last invocation the
        # total_sum/total_count, and simply returns the difference.
        delta_sum = self.derivative(delta_sum_name, total_sum,
                                    time_delta=False)
        delta_count = self.derivative(delta_count_name, total_count,
                                      time_delta=False)

        # average in the last collection interval
        if delta_count == 0:
            delta_avg = 0
        else:
            delta_avg = float(delta_sum) / float(delta_count)

        # publish raw data
        if self.config['long_running_detail']:
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
            new_name = name.__class__(name.replace("bytes", unit))
            result.append((new_name, new_value))
        return result

    def _publish_stats(self, prefix, stats, schema, name_class):
        """Publish a set of Ceph performance counters, including schema.

        :param prefix: string prefixed to metric names
        :param stats: dictionary containing performance counters
        :param schema: performance counter schema
        """
        for path, stat_type in flatten_dictionary(schema):
            # remove 'stat_type' component to get metric name
            if path[-1] != 'type':
                continue
            del path[-1]

            if stat_type & _PERFCOUNTER_LONGRUNAVG:
                self._publish_longrunavg(prefix,
                                         stats,
                                         path,
                                         stat_type,
                                         name_class)
            else:
                name = name_class(_PATH_SEP.join(filter(None, [prefix] + path)))

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
                    message = "Unexpected metric stat_type: %s/%d"
                    self.log.error(message, name, stat_type)

    def _cluster_id_prefix(self, cluster_name, fsid):
        # We'll either use the cluster name (human friendly but may not be
        # unique) or the UUID (robust but obscure)
        if self.config['short_names']:
            return cluster_name
        else:
            return fsid

    def _publish_cluster_stats(self,
                               cluster_name,
                               fsid,
                               prefix,
                               stats,
                               counter=False):
        """
        Given a stats dictionary, publish under the cluster path (respecting
        short_names and cluster_prefix)
        """

        for stat_name, stat_value in flatten_dictionary(
            stats,
            path=[self._cluster_id_prefix(cluster_name, fsid), prefix]
        ):
            stat_name = _PATH_SEP.join(stat_name)
            name = GlobalName(stat_name)
            if counter:
                self.publish_counter(name, stat_value)
            else:
                self.publish_gauge(name, stat_value)

    def _admin_command(self, socket_path, command):
        try:
            json_blob, err = _popen_check_output([self.config['ceph_binary'],
                                                  '--admin-daemon',
                                                  socket_path] + command)
        except CalledProcessError, e:
            raise AdminSocketError(socket_path, command)

        try:
            return json.loads(json_blob)
        except (ValueError, IndexError):
            self.log.exception('Error parsing output from %s' % socket_path)
            raise AdminSocketError(socket_path, command)

    def _mon_command(self, cluster, command):
        try:
            json_blob, err = _popen_check_output(
                [self.config['ceph_binary'],
                 '--cluster',
                 cluster,
                 '-f',
                 'json-pretty'] + command)
        except CalledProcessError:
            raise MonError(cluster, command)

        try:
            return json.loads(json_blob)
        except (ValueError, IndexError):
            message = 'Error parsing output from %s: %s' % (cluster, command)
            self.log.exception(message)
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
        message = "mon leader found, gathering cluster stats for cluster '%s'"
        self.log.debug(message, cluster_name)

        def publish_pool_stats(pool_id, stats):
            # Some of these guys we treat as counters, some as gauges
            delta_fields = ['num_read',
                            'num_read_kb',
                            'num_write',
                            'num_write_kb',
                            'num_objects_recovered',
                            'num_bytes_recovered',
                            'num_keys_recovered']
            for k, v in stats.items():
                self._publish_cluster_stats(cluster_name,
                                            fsid,
                                            "pool.{0}".format(pool_id),
                                            {k: v},
                                            counter=k in delta_fields)

        # Gather "ceph pg dump pools" and file the stats by pool
        for pool in self._mon_command(cluster_name, ['pg', 'dump', 'pools']):
            publish_pool_stats(pool['poolid'], pool['stat_sum'])

        all_pools_stats = self._mon_command(
            cluster_name,
            ['pg', 'dump', 'summary'])['pg_stats_sum']['stat_sum']

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

        if service_type == 'osd' and not self.config['osd_stats_enabled']:
            return

        fsid = self._admin_command(path, ['config', 'get', 'fsid'])['fsid']
        stats, schema = self._get_perf_counters(path)

        if self.config['service_stats_global']:
            counter_prefix = "{0}.{1}.{2}".format(
                self._cluster_id_prefix(cluster_name, fsid),
                service_type,
                service_id)

            self._publish_stats(counter_prefix, stats, schema, GlobalName)
        else:
            # The prefix is <cluster name>.<service type>.<service id>
            counter_prefix = "{0}.{1}.{2}".format(
                cluster_name,
                service_type,
                service_id)
            self._publish_stats(counter_prefix, stats, schema, LocalName)

    def collect(self):
        """
        Collect stats
        """
        for path in self._get_socket_paths():
            self.log.debug('gathering service stats for %s', path)

            try:
                self._collect_service_stats(path)
                self._collect_cluster_stats(path)
            except (AdminSocketError, MonError) as e:
                self.log.warn(e.__str__())
