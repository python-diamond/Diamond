
import subprocess

import diamond.collector
import socket

class MemcachedCollector(diamond.collector.Collector):
    """
    Collect memcached stats
    """

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        return {
            'enabled':  'False',
            'path':     'memcached',
            # Connection settings
            'host':     'localhost',
            'port':     '11211',
            
            # Which rows of 'status' you would like to publish.
            # 'telnet host port' and type stats and hit enter to see the list of
            # possibilities.
            # Leave unset to publish all
            #'publish': ''
        }

    def get_stats(self):
        # stuff that's always ignored, aren't 'stats'
        ignored = ('libevent', 'pid', 'pointer_size', 'time', 'version')

        config = self.config
        stats = {}
        # connect
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((config['host'], int(config['port'])))
            # request stats
            sock.send('stats\n')
            # something big enough to get whatever is sent back
            data = sock.recv(4096)
        except socket.error as e:
            self.log.exception('Failed to get stats from %s:%s',
                               config['host'], config['port'])
        else:
            # parse stats
            for line in data.split('\r\n'):
                pieces = line.split(' ')
                if pieces[0] != 'STAT' or pieces[1] in ignored:
                    continue
                stats[pieces[1]] = pieces[2]

        return stats

    def collect(self):
        stats = self.get_stats()
        # figure out what we're configured to get, defaulting to everything
        desired = self.config.get('publish', stats.keys())
        # for everything we want
        for stat in desired:
            if stat in stats:
                # we have it
                self.publish(stat, stats[stat])
            else:
                # we don't, must be somehting configured in publish so we
                # should log an error about it
                self.log.error("No such key '%s' available, issue 'stats' for "
                               "a full list", stat)

