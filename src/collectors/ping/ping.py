# coding=utf-8

"""
Collect icmp round trip times
Only valid for ipv4 hosts currently

#### Dependencies

 * ping

#### Configuration

Configuration is done by:

Create a file named: PingCollector.conf in the collectors_config_path

 * enabled = true
 * interval = 60
 * target_1 = example.org
 * target_fw = 192.168.0.1
 * target_localhost = localhost

Test your configuration using the following command:

diamond-setup --print -C PingCollector

You should get a reponse back that indicates 'enabled': True and see entries
for your targets in pairs like:

'target_1': 'example.org'

We extract out the key after target_ and use it in the graphite node we push.

"""

import subprocess
import diamond.collector
import os
from diamond.collector import str_to_bool


class PingCollector(diamond.collector.ProcessCollector):

    def get_default_config_help(self):
        config_help = super(PingCollector, self).get_default_config_help()
        config_help.update({
            'bin':         'The path to the ping binary',
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(PingCollector, self).get_default_config()
        config.update({
            'path':             'ping',
            'bin':              '/bin/ping',
        })
        return config

    def collect(self):
        for key in self.config.keys():
            if key[:7] == "target_":
                host = self.config[key]
                metric_name = host.replace('.', '_')

                ping = self.run_command(['-nq', '-c 1', host])
                ping = ping[0].strip().split("\n")[-1]

                # Linux
                if ping.startswith('rtt'):
                    ping = ping.split()[3].split('/')[0]
                    metric_value = float(ping)
                # OS X
                elif ping.startswith('round-trip '):
                    ping = ping.split()[3].split('/')[0]
                    metric_value = float(ping)
                # Unknown
                else:
                    metric_value = 10000

                self.publish(metric_name, metric_value)
