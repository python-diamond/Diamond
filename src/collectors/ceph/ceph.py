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
except ImportError:
    import simplejson as json

import glob
import os
import subprocess
import re
from distutils.version import StrictVersion


import diamond.collector


def flatten_dictionary(input, sep='.', prefix=None):
    """Produces iterator of pairs where the first value is
    the joined key names and the second value is the value
    associated with the lowest level key. For example::

      {'a': {'b': 10},
       'c': 20,
       }

    produces::

      [('a.b', 10), ('c', 20)]
    """
    for name, value in sorted(input.items()):
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
        })
        return config

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

    def _publish_stats(self, counter_prefix, stats):
        """Given a stats dictionary from _get_stats_from_socket,
        publish the individual values.
        """
        for stat_name, stat_value in flatten_dictionary(
            stats,
            prefix=counter_prefix,
        ):
            self.publish_gauge(stat_name, stat_value)

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

    def _collect_cluster_stats(self, path):
        cluster_name, service_type, service_id = self._parse_socket_name(path)
        if service_type != 'mon':
            return

        # Check if we are a high enough version to have pool throughput statistics
        version_str = self._admin_command(path, ['version'])['version']
        try:
            version = StrictVersion(version_str)
            # We expect to backport pool stats to the dumpling release series
            # in the next release, and the current release at time of writing
            # is 0.67.4.
            if version < StrictVersion("0.67.5"):
                return
        except ValueError:
            # If it doesn't parse, assume it's a git hash, therefore
            # it should be recent and have the features we want.
            pass

        # We have a mon, see if it is the leader
        mon_status = self._admin_command(path, ['mon_status'])
        if mon_status['state'] != 'leader':
            return

        self.log.debug("mon leader found, gathering cluster stats for cluster '%s'" % cluster_name)

        # We are the leader, gather cluster-wide statistics
        for pool_data in self._mon_command(cluster_name, ['osd', 'pool', 'stats']):
            pool_id = pool_data['pool_id']
            del pool_data['pool_name']
            del pool_data['pool_id']
            self._publish_stats(
                "{0}ceph.{1}.pool.{2}".format(diamond.collector.ABSOLUTE_PATH_MARKER, cluster_name, pool_id),
                pool_data
            )

        df = self._mon_command(cluster_name, ['df'])
        self._publish_stats("{0}ceph.{1}.df".format(diamond.collector.ABSOLUTE_PATH_MARKER, cluster_name), df['stats'])
        for pool_data in df['pools']:
            self._publish_stats(
                "{0}ceph.{1}.pool.{2}".format(diamond.collector.ABSOLUTE_PATH_MARKER, cluster_name, pool_data['id']),
                pool_data['stats']
            )

    def _collect_service_stats(self, path):
        # The prefix is <cluster name>.<service type>.<service id>
        counter_prefix = "{0}.{1}.{2}".format(*self._parse_socket_name(path))
        stats = self._admin_command(path, ['perf', 'dump'])
        self._publish_stats(counter_prefix, stats)

    def collect(self):
        """
        Collect stats
        """
        for path in self._get_socket_paths():
            self.log.debug('gathering service stats for %s', path)
            # Publish statistics about this service
            self._collect_service_stats(path)

            # If this service is a mon and it is the leader of a quorum, then
            # publish statistics about the cluster.
            self._collect_cluster_stats(path)