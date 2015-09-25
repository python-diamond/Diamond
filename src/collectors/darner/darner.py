# coding=utf-8

"""
Collect darner stats ( Modified from memcached collector )



#### Example Configuration

DarnerCollector.conf

```
    enabled = True
    hosts = localhost:22133, app-1@localhost:22133, app-2@localhost:22133, etc
```

TO use a unix socket, set a host string like this

```
    hosts = /path/to/blah.sock, app-1@/path/to/bleh.sock,
```
"""

import diamond.collector
import socket
import re
from diamond.collector import str_to_bool


class DarnerCollector(diamond.collector.Collector):
    GAUGES = [
        'curr_connections',
        'curr_items',
        'uptime'
    ]

    def get_default_config_help(self):
        config_help = super(DarnerCollector, self).get_default_config_help()
        config_help.update({
            'publish':
                "Which rows of 'status' you would like to publish." +
                " Telnet host port' and type stats and hit enter to see " +
                " the list of possibilities. Leave unset to publish all.",
            'hosts':
                "List of hosts, and ports to collect. Set an alias by " +
                " prefixing the host:port with alias@",
            'publish_queues':
                "Publish queue stats (defaults to True)",
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(DarnerCollector, self).get_default_config()
        config.update({
            'path':     'darner',

            # Which rows of 'status' you would like to publish.
            # 'telnet host port' and type stats and hit enter to see the list
            # of possibilities.
            # Leave unset to publish all
            # 'publish': ''
            'publish_queues': True,

            # Connection settings
            'hosts': ['localhost:22133']
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
            # request stats
            sock.send('stats\n')
            # something big enough to get whatever is sent back
            data = sock.recv(4096)
        except socket.error:
            self.log.exception('Failed to get stats from %s:%s',
                               host, port)
        return data

    def get_stats(self, host, port):
        # stuff that's always ignored, aren't 'stats'
        ignored = ('time', 'version')

        stats = {}
        queues = {}
        data = self.get_raw_stats(host, port)

        # parse stats
        for line in data.splitlines():
            pieces = line.split(' ')
            if pieces[0] != 'STAT' or pieces[1] in ignored:
                continue
            if re.match(r'^queue', pieces[1]):
                queue_match = re.match(
                    r'^queue_(.*)_(items|waiters|open_transactions)$',
                    pieces[1])
                queue_name = queue_match.group(1).replace('.', '_')
                if queue_name not in queues:
                    queues[queue_name] = {}
                queues[queue_name][queue_match.group(2)] = int(pieces[2])
            else:
                stats[pieces[1]] = int(pieces[2])
        return stats, queues

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

            stats, queues = self.get_stats(hostname, port)

            # Publish queue stats if configured
            if str_to_bool(self.config['publish_queues']):
                for queue in queues:
                    for queue_stat in queues[queue]:
                        self.publish_gauge(
                            alias + ".queues." + queue + "." + queue_stat,
                            queues[queue][queue_stat])

            # figure out what we're configured to get, defaulting to everything
            desired = self.config.get('publish', stats.keys())

            # for everything we want
            for stat in desired:
                if stat in stats:

                    # we have it
                    if stat in self.GAUGES:
                        self.publish_gauge(alias + "." + stat, stats[stat])
                    else:
                        self.publish_counter(alias + "." + stat, stats[stat])

                else:

                    # we don't, must be something configured in publish so we
                    # should log an error about it
                    self.log.error("No such key '%s' available, issue 'stats' "
                                   "for a full list", stat)
