# coding=utf-8

"""
Uses /proc/loadavg to collect data on load average

#### Dependencies

 * /proc/loadavg

"""

import diamond.collector
import re
import os

_RE = re.compile(r'([\d.]+) ([\d.]+) ([\d.]+) (\d+)/(\d+)')


class LoadAverageCollector(diamond.collector.Collector):

    PROC = '/proc/loadavg'

    def get_default_config_help(self):
        config_help = super(LoadAverageCollector,
                            self).get_default_config_help()
        config_help.update({
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(LoadAverageCollector, self).get_default_config()
        config.update({
            'enabled':  'True',
            'path':     'loadavg',
            'method':   'Threaded'
        })
        return config

    def collect(self):
        if not os.access(self.PROC, os.R_OK):
            self.log.error("Can not read path %s" % self.PROC)
            return None

        file = open(self.PROC)
        for line in file:
            match = _RE.match(line)
            if match:
                self.publish_gauge('01', float(match.group(1)), 2)
                self.publish_gauge('05', float(match.group(2)), 2)
                self.publish_gauge('15', float(match.group(3)), 2)
                self.publish_gauge('processes_running', int(match.group(4)))
                self.publish_gauge('processes_total', int(match.group(5)))
        file.close()
