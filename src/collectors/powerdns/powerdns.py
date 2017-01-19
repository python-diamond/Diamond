# coding=utf-8

"""
Collects all metrics exported by the powerdns nameserver using the
pdns_control binary.

#### Dependencies

 * pdns_control

"""

import diamond.collector
import subprocess
import os
from diamond.collector import str_to_bool


class PowerDNSCollector(diamond.collector.Collector):

    _GAUGE_KEYS = [
        'cache-bytes', 'cache-entries', 'chain-resends',
        'concurrent-queries', 'dlg-only-drops', 'dont-outqueries',
        'ipv6-outqueries', 'latency', 'max-mthread-stack', 'negcache-entries',
        'nsspeeds-entries',
        'packetcache-bytes', 'packetcache-entries', 'packetcache-size',
        'qa-latency', 'throttle-entries']

    def get_default_config_help(self):
        config_help = super(PowerDNSCollector, self).get_default_config_help()
        config_help.update({
            'bin':         'The path to the pdns_control binary',
            'use_sudo':    'Use sudo?',
            'sudo_cmd':    'Path to sudo',
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(PowerDNSCollector, self).get_default_config()
        config.update({
            'bin': '/usr/bin/pdns_control',
            'path': 'powerdns',
            'use_sudo':         False,
            'sudo_cmd':         '/usr/bin/sudo',
        })
        return config

    def collect(self):
        if not os.access(self.config['bin'], os.X_OK):
            self.log.error("%s is not executable", self.config['bin'])
            return False

        command = [self.config['bin'], 'list']

        if str_to_bool(self.config['use_sudo']):
            command.insert(0, self.config['sudo_cmd'])

        data = subprocess.Popen(command,
                                stdout=subprocess.PIPE).communicate()[0]

        for metric in data.split(','):
            if not metric.strip():
                continue
            metric, value = metric.split('=')
            try:
                value = float(value)
            except:
                pass
            if metric not in self._GAUGE_KEYS:
                value = self.derivative(metric, value)
                if value < 0:
                    continue
            self.publish(metric, value)
