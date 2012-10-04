# coding=utf-8

"""
Collect memcached stats

#### Dependencies

 * subprocess

#### Example Configuration

MemcachedCollector.conf

```
    enabled = True
    hosts = localhost:11211, app-1@localhost:11212, app-2@localhost:11213, etc
```

"""

import diamond.collector
import socket
import re


class MemcachedCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(MemcachedCollector, self).get_default_config_help()
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
        config = super(MemcachedCollector, self).get_default_config()
        config.update({
            'path':     'memcached',

            # Which rows of 'status' you would like to publish.
            # 'telnet host port' and type stats and hit enter to see the list of
            # possibilities.
            # Leave unset to publish all
            #'publish': ''

            # Connection settings
            'hosts': [ 'localhost:11211' ]
        })
        return config

    def get_raw_stats(self, host, port):
        data = ''
        # connect
        try:
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
        ignored = ('libevent', 'pid', 'pointer_size', 'time', 'version')

        stats = {}
        data = self.get_raw_stats(host, int(port))

        # parse stats
        for line in data.splitlines():
            pieces = line.split(' ')
            if pieces[0] != 'STAT' or pieces[1] in ignored:
                continue
            stats[pieces[1]] = pieces[2]

        return stats

    def collect(self):
        hosts = self.config.get('hosts')
        
        # Convert a string config value to be an array
        if isinstance(hosts, basestring):
            hosts = [hosts]
            
        for host in hosts:
            matches = re.search('((.+)\@)?([^:]+):(\d+)', host)
            alias = matches.group(2)
            hostname = matches.group(3)
            port = matches.group(4)
            
            if alias is None:
                alias = hostname
            
            stats = self.get_stats(hostname, port)
            
            # figure out what we're configured to get, defaulting to everything
            desired = self.config.get('publish', stats.keys())
            
            # for everything we want
            for stat in desired:
                if stat in stats:
                    
                    # we have it
                    self.publish(alias + "." + stat, stats[stat])
                else:
                    
                    # we don't, must be somehting configured in publish so we
                    # should log an error about it
                    self.log.error("No such key '%s' available, issue 'stats' "
                                   "for a full list", stat)
