# coding=utf-8

"""
The IPCollector class collects metrics on IP stats

#### Dependencies

 * /proc/net/snmp

#### Allowed Metric Names
<table>
<tr><th>Name</th></tr>
<tr><th>InAddrErrors</th></tr>
<tr><th>InDelivers</th></tr>
<tr><th>InDiscards</th></tr>
<tr><th>InHdrErrors</th></tr>
<tr><th>InReceives</th></tr>
<tr><th>InUnknownProtos</th></tr>
<tr><th>OutDiscards</th></tr>
<tr><th>OutNoRoutes</th></tr>
<tr><th>OutRequests</th></tr>
</table>

"""

import diamond.collector
import os


class IPCollector(diamond.collector.Collector):

    PROC = [
        '/proc/net/snmp',
    ]

    GAUGES = [
        'Forwarding',
        'DefaultTTL',
    ]

    def process_config(self):
        if self.config['allowed_names'] is None:
            self.config['allowed_names'] = []

    def get_default_config_help(self):
        config_help = super(IPCollector, self).get_default_config_help()
        config_help.update({
            'allowed_names': 'list of entries to collect, empty to collect all'
        })
        return config_help

    def get_default_config(self):
        ''' Returns the default collector settings
        '''
        config = super(IPCollector, self).get_default_config()
        config.update({
            'path': 'ip',
            'allowed_names': 'InAddrErrors, InDelivers, InDiscards, '
            + 'InHdrErrors, InReceives, InUnknownProtos, OutDiscards, '
            + 'OutNoRoutes, OutRequests'
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

            # Seek the file for the lines which start with Ip
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
                if line.startswith('Ip'):
                    header = line
                    data = file.readline()
                    break
            file.close()

            # No data from the file?
            if header == '' or data == '':
                self.log.error('%s has no lines starting with Ip' % filepath)
                continue

            header = header.split()
            data = data.split()

            # Zip up the keys and values
            for i in xrange(1, len(header)):
                metrics[header[i]] = data[i]

        for metric_name in metrics.keys():
            if (len(self.config['allowed_names']) > 0
                    and metric_name not in self.config['allowed_names']):
                continue

            value = long(metrics[metric_name])

            # Publish the metric
            if metric_name in self.GAUGES:
                self.publish_gauge(metric_name, value, 0)
            else:
                self.publish_counter(metric_name, value, 0)
