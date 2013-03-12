# coding=utf-8

"""
Collect zookeeper stats. ( Modified from memcached collector )

#### Dependencies

 * subprocess

#### Example Configuration

ZookeeperCollector.conf

```
    enabled = True
    hosts = localhost:2181, app-1@localhost:2181, app-2@localhost:2181, etc
```

TO use a unix socket, set a host string like this

```
    hosts = /path/to/blah.sock, app-1@/path/to/bleh.sock,
```
"""

import diamond.collector
import socket
import re


class ZookeeperCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(ZookeeperCollector, self).get_default_config_help()
        config_help.update({
            'publish': "Which rows of 'status' you would like to publish."
            + " Telnet host port' and type stats and hit enter to see the list"
            + " of possibilities. Leave unset to publish all.",
            'hosts': "List of hosts, and ports to collect. Set an alias by "
            + " prefixing the host:port with alias@",
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(ZookeeperCollector, self).get_default_config()
        config.update({
            'path':     'zookeeper',

            # Which rows of 'status' you would like to publish.
            # 'telnet host port' and type mntr and hit enter to see the list of
            # possibilities.
            # Leave unset to publish all
            #'publish': ''

            # Connection settings
            'hosts': ['localhost:2181']
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
            sock.send('mntr\n')
            # something big enough to get whatever is sent back
            data = sock.recv(4096)
        except socket.error:
            self.log.exception('Failed to get stats from %s:%s',
                               host, port)
        return data

    def get_stats(self, host, port):
        # stuff that's always ignored, aren't 'stats'
        ignored = ('zk_version', 'zk_server_state')
        pid = None

        stats = {}
        data = self.get_raw_stats(host, port)

        # parse stats
        for line in data.splitlines():

            pieces = line.split()

            if pieces[0] in ignored:
                continue
            stats[pieces[0]] = pieces[1]

        # get max connection limit
        self.log.debug('pid %s', pid)
        try:
            cmdline = "/proc/%s/cmdline" % pid
            f = open(cmdline, 'r')
            m = re.search("-c\x00(\d+)", f.readline())
            if m is not None:
                self.log.debug('limit connections %s', m.group(1))
                stats['limit_maxconn'] = m.group(1)
            f.close()
        except:
            self.log.debug("Cannot parse command line options for zookeeper")

        return stats

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

            stats = self.get_stats(hostname, port)

            # figure out what we're configured to get, defaulting to everything
            desired = self.config.get('publish', stats.keys())

            # for everything we want
            for stat in desired:
                if stat in stats:

                    # we have it
                    if alias is not None:
                        self.publish(alias + "." + stat, stats[stat])
                    else:
                        self.publish(stat, stats[stat])
                else:

                    # we don't, must be somehting configured in publish so we
                    # should log an error about it
                    self.log.error("No such key '%s' available, issue 'stats' "
                                   "for a full list", stat)
