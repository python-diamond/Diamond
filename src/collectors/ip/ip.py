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

    PROC6 = [
        '/proc/net/snmp6'
    ]

    GAUGES = [
        'Forwarding',
        'DefaultTTL',
    ]

    DEFAULT_METRICS = [
        'InAddrErrors', 'InDelivers', 'InDiscards', 'InHdrErrors',
        'InReceives', 'InUnknownProtos', 'OutDiscards', 'OutNoRoutes',
        'OutRequests',
        'Ip6InAddrErrors', 'Ip6InDelivers', 'Ip6InDiscards',
        'Ip6InHdrErrors', 'Ip6InReceives', 'Ip6InUnknownProtos',
        'Ip6OutDiscards', 'Ip6OutNoRoutes', 'Ip6OutRequests'
    ]

    def process_config(self):
        super(IPCollector, self).process_config()
        if self.config['allowed_names'] is None:
            self.config['allowed_names'] = []

    def get_default_config_help(self):
        config_help = super(IPCollector, self).get_default_config_help()
        config_help.update({
            'allowed_names': 'list of entries to collect, empty to collect all'
        })
        return config_help

    def get_default_config(self):
        """ Returns the default collector settings
        """
        config = super(IPCollector, self).get_default_config()
        config.update({
            'path': 'ip',
            'allowed_names': ','.join(self.DEFAULT_METRICS)
        })
        return config

    def open_file(self, filepath):
        if not os.access(filepath, os.R_OK):
            self.log.error('Permission to access %s denied', filepath)
            return

        fp = open(filepath)

        if not fp:
            self.log.error('Failed to open %s', filepath)
            return
        return fp

    def collect(self):
        self.collect_ipv4()
        self.collect_ipv6()

    def collect_ipv4(self):
        metrics = {}

        for filepath in self.PROC:
            file = self.open_file(filepath)
            if not file:
                continue

            header = ''
            data = ''

            # Seek the file for the lines which start with Ip
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
            if ((len(self.config['allowed_names']) > 0 and
                 metric_name not in self.config['allowed_names'])):
                continue

            value = long(metrics[metric_name])

            # Publish the metric
            if metric_name in self.GAUGES:
                self.publish_gauge(metric_name, value, 0)
            else:
                self.publish_counter(metric_name, value, 0)

    def collect_ipv6(self):
        metrics = {}
        for filepath in self.PROC6:
            fp = self.open_file(filepath)

            for line in fp.readlines():
                key, value = line.split()
                metrics[key] = long(value)

            fp.close()

        for metric, value in metrics.iteritems():
            if (len(self.config['allowed_names']) > 0
                    and metric not in self.config['allowed_names']):
                continue

            # Publish the metric
            if metric in self.GAUGES:
                self.publish_gauge(metric, value, 0)
            else:
                self.publish_counter(metric, value, 0)
