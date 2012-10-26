# coding=utf-8

"""
This collector uses the [ipmitool](http://openipmi.sourceforge.net/) to read
hardware sensors from servers
using the Intelligent Platform Management Interface (IPMI). IPMI is very common
with server hardware but usually not available in consumer hardware.

#### Dependencies

 * [ipmitool](http://openipmi.sourceforge.net/)

"""

import diamond.collector
import subprocess
import os
import re
import getpass


class IPMISensorCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(IPMISensorCollector, self).get_default_config_help()
        config_help.update({
            'bin': 'Path to the ipmitool binary',
            'use_sudo': 'Use sudo?',
            'sudo_cmd': 'Path to sudo',
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(IPMISensorCollector, self).get_default_config()
        config.update({
            'bin':              '/usr/bin/ipmitool',
            'use_sudo':         False,
            'sudo_cmd':         '/usr/bin/sudo',
            'path':             'ipmi.sensors'
        })
        return config

    def collect(self):
        if (not os.access(self.config['bin'], os.X_OK)
            or (self.config['use_sudo']
                and not os.access(self.config['sudo_cmd'], os.X_OK))):
            return False

        command = [self.config['bin'], 'sensor']

        if self.config['use_sudo'] and getpass.getuser() != 'root':
            command.insert(0, self.config['sudo_cmd'])

        p = subprocess.Popen(command,
                             stdout=subprocess.PIPE).communicate()[0][:-1]

        for i, v in enumerate(p.split("\n")):
            data = v.split("|")
            try:
                # Complex keys are fun!
                metric_name = data[0].strip().replace(".",
                                                      "_").replace(" ", ".")
                value = data[1].strip()

                # Skip missing sensors
                if value == '0x0' or value == 'na':
                    continue

                # Extract out a float value
                vmatch = re.search("([0-9.]+)", value)
                if not vmatch:
                    continue
                metric_value = float(vmatch.group(1))

                # Publish
                self.publish(metric_name, metric_value)
            except ValueError:
                continue
            except IndexError:
                continue

        return True
