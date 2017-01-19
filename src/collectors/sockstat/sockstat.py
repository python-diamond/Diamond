# coding=utf-8

"""
Uses /proc/net/sockstat to collect data on number of open sockets

#### Dependencies

 * /proc/net/sockstat

"""

import diamond.collector
import re
import os
from collections import defaultdict


_RE = re.compile('|'.join([
    r'sockets: used (?P<used>\d+)?',
    r'(TCP|TCP6): inuse (?P<tcp_inuse>\d+)' +
    r'( orphan (?P<tcp_orphan>\d+) ' +
    r'tw (?P<tcp_tw>\d+) ' +
    r'alloc (?P<tcp_alloc>\d+) ' +
    r'mem (?P<tcp_mem>\d+))?',
    r'(UDP|UDP6): inuse (?P<udp_inuse>\d+)( mem (?P<udp_mem>\d+))?'
]))


class SockstatCollector(diamond.collector.Collector):

    PROCS = ['/proc/net/sockstat', '/proc/net/sockstat6']

    def get_default_config_help(self):
        config_help = super(SockstatCollector, self).get_default_config_help()
        config_help.update({
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(SockstatCollector, self).get_default_config()
        config.update({
            'path':     'sockets',
        })
        return config

    def collect(self):

        result = defaultdict(int)
        for path in self.PROCS:
            if not os.access(path, os.R_OK):
                continue

            f = open(path)
            self.collect_stat(result, f)
            f.close()

        for key, value in result.items():
            self.publish(key, value, metric_type='GAUGE')

    def collect_stat(self, data, f):

        for line in f:
            match = _RE.match(line)
            if match:
                for key, value in match.groupdict().items():
                    if value:
                        data[key] += int(value)
