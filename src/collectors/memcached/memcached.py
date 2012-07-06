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
        config = super(MemcachedCollector, self).get_default_config()
        config.update(  {
            'path':     'memcached',
            
            # Which rows of 'status' you would like to publish.
            # 'telnet host port' and type stats and hit enter to see the list of
            # possibilities.
            # Leave unset to publish all
            #'publish': ''
            
            # Connection settings
            'hosts':    {
                'localhost': {
                    'host':     'localhost',
                    'port':     '11211',
                },
            },
        } )
        return config

    def get_stats(self, config):
        # stuff that's always ignored, aren't 'stats'
        ignored = ('libevent', 'pid', 'pointer_size', 'time', 'version')
        
        stats = {}
        # connect
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((config['host'], int(config['port'])))
            # request stats
            sock.send('stats\n')
            # something big enough to get whatever is sent back
            data = sock.recv(4096)
        except socket.error, e:
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
        hosts = self.config.get('hosts')
        for host in hosts:
            stats = self.get_stats(hosts[host])
            # figure out what we're configured to get, defaulting to everything
            desired = self.config.get('publish', stats.keys())
            # for everything we want
            for stat in desired:
                if stat in stats:
                    # we have it
                    self.publish(host+"."+stat, stats[stat])
                else:
                    # we don't, must be somehting configured in publish so we
                    # should log an error about it
                    self.log.error("No such key '%s' available, issue 'stats' for "
                                   "a full list", stat)

