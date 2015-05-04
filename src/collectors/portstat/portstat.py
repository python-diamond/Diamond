"""
The PortStatCollector collects metrics about ports listed in config file.

##### Dependencies

* psutil

"""

from collections import defaultdict
import diamond.collector

try:
    import psutil
except ImportError:
    psutil = None


def get_port_stats(port):
    """
    Iterate over connections and count states for specified port
    :param port: port for which stats are collected
    :return: Counter with port states
    """
    cnts = defaultdict(int)
    for c in psutil.net_connections():
        c_port = c.laddr[1]
        if c_port != port:
            continue
        status = c.status.lower()
        cnts[status] += 1
    return cnts


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

    def collect(self):
        """
        Overrides the Collector.collect method
        """

        if psutil is None:
            self.log.error('Unable to import module psutil')
            return {}

        for port_name, port_cfg in self.ports.iteritems():
            port = int(port_cfg['number'])
            stats = get_port_stats(port)

            for stat_name, stat_value in stats.iteritems():
                metric_name = '%s.%s' % (port_name, stat_name)
                self.publish(metric_name, stat_value)
