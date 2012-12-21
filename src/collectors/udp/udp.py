# coding=utf-8

"""
The UDPCollector class collects metrics on UDP stats (surprise!)

#### Dependencies

 * /proc/net/snmp

"""

import diamond.collector
import os


class UDPCollector(diamond.collector.Collector):

    PROC = '/proc/net/snmp'

    def get_default_config_help(self):
        config_help = super(UDPCollector, self).get_default_config_help()
        config_help.update({
            'allowed_names': 'list of entries to collect',
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(UDPCollector, self).get_default_config()
        config.update({
            'path':             'udp',
            'allowed_names':    'InDatagrams, NoPorts, '
            + 'InErrors, OutDatagrams, RcvbufErrors, SndbufErrors'
        })
        return config

    def collect(self):
        if not os.access(self.PROC, os.R_OK):
            return None

        lines = []

        file = open(self.PROC)
        for line in file:
            if line.startswith("Udp:"):
                lines.append(line[5:].split())
        file.close()

        if len(lines) != 2:
            return

        # There are two lines in lines: names and values, space-separated.
        names, values = lines
        allowed_names = self.config['allowed_names']

        for key, value in zip(names, values):
            if key in allowed_names:
                value = self.derivative(key, long(value))
                if value < 0:
                    continue
                self.publish(key, value, 0)
