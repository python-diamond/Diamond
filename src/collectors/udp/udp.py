# coding=utf-8

"""
The UDPCollector class collects metrics on UDP stats (surprise!)

#### Dependencies

 * /proc/net/snmp

"""

import diamond.collector
import os


class UDPCollector(diamond.collector.Collector):

    PROC = [
        '/proc/net/snmp'
    ]

    def process_config(self):
        if self.config['allowed_names'] is None:
            self.config['allowed_names'] = []

    def get_default_config_help(self):
        config_help = super(UDPCollector, self).get_default_config_help()
        config_help.update({
            'allowed_names': 'list of entries to collect, empty to collect all',
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
        metrics = {}

        for filepath in self.PROC:
            if not os.access(filepath, os.R_OK):
                self.log.error('Permission to access %s denied', filepath)
                continue

            header = ''
            data = ''

            # Seek the file for the lines that start with Tcp
            file = open(filepath)

            if not file:
                self.log.error('Failed to open %s', filepath)
                continue

            while True:
                line = file.readline()

                # Reached EOF?
                if len(line) == 0:
                    break

                # Line has metrics?
                if line.startswith("Udp"):
                    header = line
                    data = file.readline()
                    break
            file.close()

            # No data from the file?
            if header == '' or data == '':
                self.log.error('%s has no lines with Udp', filepath)
                continue

            header = header.split()
            data = data.split()

            for i in xrange(1, len(header)):
                metrics[header[i]] = data[i]

        for metric_name in metrics.keys():
            if (len(self.config['allowed_names']) > 0
                    and metric_name not in self.config['allowed_names']):
                continue

            value = metrics[metric_name]
            value = self.derivative(metric_name, long(value))

            # Publish the metric
            self.publish(metric_name, value, 0)
