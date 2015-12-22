# coding=utf-8

"""
Collect twemproxy (aka nutcracker) stats ( Modified from memcached collector )

#### Dependencies

 * json or simplejson

#### Example Configuration

TwemproxyCollector.conf

```
    enabled = True
    hosts = localhost:22222, app-1@localhost:22222, app-2@localhost:22222, etc
```

TO use a unix socket, set a host string like this

```
    hosts = /path/to/blah.sock, app-1@/path/to/bleh.sock,
```
"""

import diamond.collector
import socket
import re

try:
    import simplejson as json
except ImportError:
    import json


class TwemproxyCollector(diamond.collector.Collector):
    GAUGES = [
        'uptime',
        'curr_connections',
        'client_connections',
        'server_connections',
        'server_ejected_at',
        'in_queue',
        'in_queue_bytes',
        'out_queue',
        'out_queue_bytes'
    ]

    IGNORED = [
        'service',
        'source',
        'timestamp',
        'version'
    ]

    def get_default_config_help(self):
        config_help = super(TwemproxyCollector, self).get_default_config_help()
        config_help.update({
            'hosts': "List of hosts, and ports to collect. Set an alias by " +
            " prefixing the host:port with alias@",
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(TwemproxyCollector, self).get_default_config()
        config.update({
            'path':     'twemproxy',
            'hosts': ['localhost:22222']
        })
        return config

    def get_raw_stats(self, host, port):
        data = ''
        # connect
        try:
            if port is None:
                sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                sock.connect(host)
            else:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((host, int(port)))

            stats_data = ''
            while True:
                data = sock.recv(1024)
                if not data:
                    break
                stats_data += data
            sock.close()

        except socket.error:
            self.log.exception('Failed to get stats from %s:%s',
                               host, port)

        try:
            return json.loads(stats_data)
        except (TypeError, ValueError):
            self.log.error("Unable to parse response from Twemproxy as a"
                           " json object")
            return False

    def get_stats(self, host, port):
        stats = {}
        pools = {}
        data = self.get_raw_stats(host, port)

        if data is None:
            self.log.error('Unable to import json')
            return {}

        stats = {}
        pools = {}
        for stat, value in data.iteritems():
            # Test if this is a pool
            if isinstance(value, dict):
                pool_name = stat.replace('.', '_')
                pools[pool_name] = {}
                for pool_stat, pool_value in value.iteritems():
                    # Test if this is a pool server
                    if isinstance(pool_value, dict):
                        server_name = pool_stat.replace('.', '_')
                        pools[pool_name][server_name] = {}
                        for server_stat, server_value in pool_value.iteritems():
                            pools[pool_name][server_name][server_stat] = \
                                int(server_value)
                    else:
                        pools[pool_name][pool_stat] = int(pool_value)
            else:
                if stat in self.IGNORED:
                    continue
                else:
                    stats[stat] = int(value)

        return stats, pools

    def collect(self):
        hosts = self.config.get('hosts')

        # Convert a string config value to be an array
        if isinstance(hosts, basestring):
            hosts = [hosts]

        for host in hosts:
            matches = re.search('((.+)\@)?([^:]+)(:(\d+))?', host)
            alias = matches.group(2)
            hostname = matches.group(3)
            port = matches.group(5)

            if alias is None:
                alias = hostname

            stats, pools = self.get_stats(hostname, port)

            for stat in stats:
                if stat in self.GAUGES:
                    self.publish_gauge(alias + "." + stat, stats[stat])
                else:
                    self.publish_counter(alias + "." + stat, stats[stat])

            # Pool stats
            for pool, pool_stats in pools.iteritems():
                for stat, stat_value in pool_stats.iteritems():
                    # Test if this is a pool server
                    if isinstance(stat_value, dict):
                        for server_stat, server_value in stat_value.iteritems():
                            if server_stat in self.GAUGES:
                                self.publish_gauge(
                                    alias + ".pools." + pool + ".servers." +
                                    stat + "." + server_stat, server_value)
                            else:
                                self.publish_counter(
                                    alias + ".pools." + pool + ".servers." +
                                    stat + "." + server_stat, server_value)
                    else:
                        if stat in self.GAUGES:
                            self.publish_gauge(
                                alias + ".pools." + pool + "." + stat,
                                stat_value)
                        else:
                            self.publish_counter(
                                alias + ".pools." + pool + "." + stat,
                                stat_value)
