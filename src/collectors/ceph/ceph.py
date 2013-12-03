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
from collections import defaultdict
from distutils.version import StrictVersion
import diamond.collector


def flatten_dictionary(input_dict, sep='.', prefix=None):
    """Produces iterator of pairs where the first value is
    the joined key names and the second value is the value
    associated with the lowest level key. For example::

      {'a': {'b': 10},
       'c': 20,
       }

    produces::

      [('a.b', 10), ('c', 20)]
    """
    for name, value in sorted(input_dict.items()):
        fullname = sep.join(filter(None, [prefix, name]))
        if isinstance(value, dict):
            for result in flatten_dictionary(value, sep, fullname):
                yield result
        else:
            yield (fullname, value)


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
            'service_stats_global': False
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

    def _publish_stats(self, counter_prefix, stats, global_name=False):
        """Given a stats dictionary from _get_stats_from_socket,
        publish the individual values.
        """
        for stat_name, stat_value in flatten_dictionary(
            stats,
            prefix=counter_prefix,
        ):
            self.publish_gauge(GlobalName(stat_name) if global_name else stat_name, stat_value)

    def _publish_cluster_stats(self, cluster_name, fsid, prefix, stats):
        """
        Given a stats dictionary, publish under the cluster path (respecting
        short_names and cluster_prefix
        """
        # We'll either use the cluster name (human friendly but may not be unique)
        # or the UUID (robust but obscure)
        if self.config['short_names']:
            cluster_id_prefix = cluster_name
        else:
            cluster_id_prefix = fsid

        self._publish_stats("{0}.{1}".format(cluster_id_prefix, prefix), stats, global_name=True)

    def _admin_command(self, socket_path, command):
        try:
            json_blob = subprocess.check_output(
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
            json_blob = subprocess.check_output(
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

        # Check if we are a high enough version to have pool throughput statistics
        version_str = self._admin_command(path, ['version'])['version']
        try:
            version = StrictVersion(version_str)
        except ValueError:
            # In case it's a git hash or something like that
            version = None

        # We have a mon, see if it is the leader
        mon_status = self._admin_command(path, ['mon_status'])
        if mon_status['state'] != 'leader':
            return
        fsid = mon_status['monmap']['fsid']

        # We are the leader, gather cluster-wide statistics
        self.log.debug("mon leader found, gathering cluster stats for cluster '%s'" % cluster_name)

        # Recent Ceph versions have some per-pool statistics for us
        if version is None or version >= StrictVersion("0.67.5"):
            # Not everything in the pool stats makes sense to sum (e.g. ratios), so
            # we have an explicit list of which items to put into the 'all' pool.
            aggregates = {
                'client_io_rate': {
                    'op_per_sec': 0,
                    'write_bytes_sec': 0,
                    'read_bytes_sec': 0
                },
                'recovery': {
                    'degraded_objects': 0,
                    'degraded_total': 0,
                },
                'recovery_rate': {
                    'recovering_objects_per_sec': 0,
                    'recovering_keys_per_sec': 0,
                    'recovering_bytes_per_sec': 0,
                }
            }
            for pool_data in self._mon_command(cluster_name, ['osd', 'pool', 'stats']):
                pool_id = pool_data['pool_id']
                del pool_data['pool_name']
                del pool_data['pool_id']

                for k, v in aggregates.items():
                    if k in pool_data:
                        pool_data_k = pool_data[k]
                        for k2, v2 in v.items():
                            if k2 in pool_data_k:
                                v[k2] += pool_data_k[k2]

                self._publish_cluster_stats(cluster_name, fsid,
                                            "pool.{0}".format(pool_id),
                                            pool_data)
            self._publish_cluster_stats(cluster_name, fsid,
                                        "pool.all",
                                        aggregates)

        # Older Ceph versions only give us some global throughput stats
        if version <= StrictVersion("0.67.4"):
            summary = self._mon_command(cluster_name, ['pg', 'dump', 'summary'])
            pg_stats_delta = summary['pg_stats_delta']['stat_sum']

            # We will synthesize the 'client_io_rate.op_per_sec' statistic that
            # would otherwise come from 'osd pool stats'
            tick_period = 5.0  # We assume this has been left as the default
            op_per_sec = (pg_stats_delta['num_write'] + pg_stats_delta['num_read']) / tick_period
            self._publish_cluster_stats(cluster_name, fsid,
                                        "pool.all",
                                        {'client_io_rate': {"op_per_sec": op_per_sec}})

        # Gather "ceph df" and file the stats by pool
        df = self._mon_command(cluster_name, ['df'])
        self._publish_cluster_stats(cluster_name, fsid, "df", df['stats'])
        all_pools_df = defaultdict(int)
        for pool_data in df['pools']:
            self._publish_cluster_stats(cluster_name, fsid,
                                        "pool.{0}".format(pool_data['id']),
                                        pool_data['stats'])

            for k, v in pool_data['stats'].items():
                all_pools_df[k] += v
        self._publish_cluster_stats(cluster_name, fsid,
                                    "pool.all",
                                    all_pools_df)

    def _collect_service_stats(self, path):
        cluster_name, service_type, service_id = self._parse_socket_name(path)
        fsid = self._admin_command(path, ['config', 'get', 'fsid'])['fsid']

        stats = self._admin_command(path, ['perf', 'dump'])
        if self.config['service_stats_global']:
            counter_prefix = "{0}.{1}".format(service_type, service_id)
            self._publish_cluster_stats(cluster_name, fsid, counter_prefix, stats)
        else:
            # The prefix is <cluster name>.<service type>.<service id>
            counter_prefix = "{0}.{1}.{2}".format(*self._parse_socket_name(path))
            self._publish_stats(counter_prefix, stats)

    def collect(self):
        """
        Collect stats
        """
        for path in self._get_socket_paths():
            self.log.debug('gathering service stats for %s', path)

            self._collect_service_stats(path)
            self._collect_cluster_stats(path)
