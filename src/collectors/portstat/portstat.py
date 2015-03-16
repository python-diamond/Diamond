"""
The PortStatCollector collects metrics about ports listed in config file.

##### Dependencies

* psutil

"""

from collections import Counter

import psutil
import diamond.collector


class PortStatCollector(diamond.collector.Collector):

    def __init__(self, *args, **kwargs):
        super(PortStatCollector, self).__init__(*args, **kwargs)
        self.ports = {}
        for port_name, cfg in self.config['port'].items():
            port_cfg = {}
            for key in ('number',):
                port_cfg[key] = cfg.get(key, [])
            self.ports[port_name] = port_cfg

    def get_default_config_help(self):
        config_help = super(PortStatCollector, self).get_default_config_help()
        config_help.update({
        })
        return config_help

    def get_default_config(self):
        config = super(PortStatCollector, self).get_default_config()
        config.update({
            'path': 'port',
            'port': {},
        })
        return config

    @staticmethod
    def get_port_stats(port):
        """
        Iterate over connections and count states for specified port
        :param port: port for which stats are collected
        :return: Counter with port states
        """
        cnts = Counter()
        for c in psutil.net_connections():
            c_port = c.laddr[1]
            if c_port != port:
                continue
            status = c.status.lower()
            cnts[status] += 1
        return cnts

    def collect(self):
        """
        Overrides the Collector.collect method
        """

        for port_name, port_cfg in self.ports.iteritems():
            port = int(port_cfg['number'])
            stats = PortStatCollector.get_port_stats(port)

            for stat_name, stat_value in stats.iteritems():
                metric_name = '%s.%s' % (port_name, stat_name)
                self.publish(metric_name, stat_value)
