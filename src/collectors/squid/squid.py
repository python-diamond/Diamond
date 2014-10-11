# coding=utf-8

"""
Collects data from squid servers

#### Dependencies

"""

import re
import socket
import diamond.collector


class SquidCollector(diamond.collector.Collector):

    def __init__(self, *args, **kwargs):
        self.host_pattern = re.compile("(([^@]+)@)?([^:]+)(:([0-9]+))?")
        self.stat_pattern = re.compile("^([^ ]+) = ([0-9\.]+)$")

        super(SquidCollector, self).__init__(*args, **kwargs)

    def process_config(self):
        self.squid_hosts = {}

        for host in self.config['hosts']:
            matches = self.host_pattern.match(host)

            if matches.group(5):
                port = matches.group(5)
            else:
                port = 3128

            if matches.group(2):
                nick = matches.group(2)
            else:
                nick = port

            self.squid_hosts[nick] = {
                'host': matches.group(3),
                'port': int(port)
            }

    def get_default_config_help(self):
        config_help = super(SquidCollector, self).get_default_config_help()
        config_help.update({
            'hosts': 'List of hosts to collect from. Format is '
            + '[nickname@]host[:port], [nickname@]host[:port], etc',
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(SquidCollector, self).get_default_config()
        config.update({
            'hosts': ['localhost:3128'],
            'path': 'squid',
        })
        return config

    def _getData(self, host, port):
        try:
            squid_sock = socket.socket()
            squid_sock.connect((host, int(port)))
            squid_sock.settimeout(0.25)
            squid_sock.sendall("GET cache_object://localhost/counters HTTP/1.0"
                               + "\r\nHost: localhost\r\nAccept: */*\r\nConnec"
                               + "tion: close\r\n\r\n")

            fulldata = ''

            while True:
                data = squid_sock.recv(1024)
                if not data:
                    break
                fulldata = fulldata + data
        except Exception, e:
            self.log.error('Couldnt connect to squid: %s', e)
            return None
        squid_sock.close()

        return fulldata

    def collect(self):
        for nickname in self.squid_hosts.keys():
            squid_host = self.squid_hosts[nickname]

            fulldata = self._getData(squid_host['host'],
                                     squid_host['port'])

            if fulldata is not None:
                fulldata = fulldata.splitlines()

                for data in fulldata:
                    matches = self.stat_pattern.match(data)
                    if matches:
                        self.publish_counter("%s.%s" % (nickname,
                                                        matches.group(1)),
                                             float(matches.group(2)))
