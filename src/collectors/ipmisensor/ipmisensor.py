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
from subprocess import Popen, PIPE
import os
import getpass


class IPMISensorCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(IPMISensorCollector,
                            self).get_default_config_help()
        config_help.update({
            'bin': 'Path to the ipmitool binary',
            'use_sudo': 'Use sudo?',
            'sudo_cmd': 'Path to sudo',
            'thresholds': 'Collect thresholds as well as reading'
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
            'path':             'ipmi.sensors',
            'thresholds':       False,
        })
        return config

    def parse_value(self, value):
        """
        Convert value string to float for reporting
        """
        value = value.strip()

        # Skip missing sensors
        if value == 'na':
            return None

        # Try just getting the float value
        try:
            return float(value)
        except:
            pass

        # Next best guess is a hex value
        try:
            return float.fromhex(value)
        except:
            pass

        # No luck, bail
        return None

    def collect(self):
        if (not os.access(self.config['bin'], os.X_OK)
            or (self.config['use_sudo']
                and not os.access(self.config['sudo_cmd'], os.X_OK))):
            return False

        command = [self.config['bin'], 'sensor']

        if self.config['use_sudo'] and getpass.getuser() != 'root':
            command.insert(0, self.config['sudo_cmd'])

        p = Popen(command, stdout=PIPE).communicate()[0][:-1]

        for i, v in enumerate(p.split("\n")):
            data = v.split("|")
            try:
                # Complex keys are fun!
                metric_name = data[0].strip().replace(".",
                                                      "_").replace(" ", ".")
                metrics = []

                # Each sensor line is a column seperated by a | with the
                # following descriptions:
                # 1. Sensor ID
                # 2. Sensor Reading
                # 3. Units
                # 4. Status
                # 5. Lower Non-Recoverable
                # 6. Lower Critical
                # 7. Lower Non-Critical
                # 8. Upper Non-Critical
                # 9. Upper Critical
                # 10. Upper Non-Recoverable

                if not self.config['thresholds']:
                    metrics.append((metric_name, self.parse_value(data[1])))
                else:
                    metrics.append((metric_name + ".Reading",
                                    self.parse_value(data[1])))
                    metrics.append((metric_name + ".Lower.NonRecoverable",
                                    self.parse_value(data[4])))
                    metrics.append((metric_name + ".Lower.Critical",
                                    self.parse_value(data[5])))
                    metrics.append((metric_name + ".Lower.NonCritical",
                                    self.parse_value(data[6])))
                    metrics.append((metric_name + ".Upper.NonCritical",
                                    self.parse_value(data[7])))
                    metrics.append((metric_name + ".Upper.Critical",
                                    self.parse_value(data[8])))
                    metrics.append((metric_name + ".Upper.NonRecoverable",
                                    self.parse_value(data[9])))

                [self.publish(name, value)
                 for (name, value) in metrics
                 if value is not None]

            except ValueError:
                continue
            except IndexError:
                continue

        return True
