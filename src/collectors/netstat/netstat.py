# coding=utf-8

"""
The NetstatCollector class collects metrics on number of connections
in each state

#### Dependencies

 * /proc/net/tcp

Based on Ricardo Pascal's "netstat in <100 lines of code"

"""

import diamond.collector


class NetstatCollector(diamond.collector.Collector):
    PROC_TCP = "/proc/net/tcp"
    STATE = {
        '01': 'ESTABLISHED',
        '02': 'SYN_SENT',
        '03': 'SYN_RECV',
        '04': 'FIN_WAIT1',
        '05': 'FIN_WAIT2',
        '06': 'TIME_WAIT',
        '07': 'CLOSE',
        '08': 'CLOSE_WAIT',
        '09': 'LAST_ACK',
        '0A': 'LISTEN',
        '0B': 'CLOSING'
    }

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(NetstatCollector, self).get_default_config()
        config.update({
            'path':         'netstat',
        })
        return config

    def collect(self):
        """
        Overrides the Collector.collect method
        """

        content = self._load()
        result = dict((self.STATE[num], 0) for num in self.STATE)

        for line in content:
            line_array = self._remove_empty(line.split(' '))
            state = self.STATE[line_array[3]]

            result[state] += 1

        for state in result:
            self.publish(state, result[state])

    @staticmethod
    def _load():
        """ Read the table of tcp connections & remove header  """
        with open(NetstatCollector.PROC_TCP, 'r') as f:
            content = f.readlines()
            content.pop(0)
        return content

    @staticmethod
    def _hex2dec(s):
        return str(int(s, 16))

    @staticmethod
    def _ip(s):
        ip = [(NetstatCollector._hex2dec(s[6:8])),
              (NetstatCollector._hex2dec(s[4:6])),
              (NetstatCollector._hex2dec(s[2:4])),
              (NetstatCollector._hex2dec(s[0:2]))]
        return '.'.join(ip)

    @staticmethod
    def _remove_empty(array):
        return [x for x in array if x != '']

    @staticmethod
    def _convert_ip_port(array):
        host, port = array.split(':')
        return NetstatCollector._ip(host), NetstatCollector._hex2dec(port)
