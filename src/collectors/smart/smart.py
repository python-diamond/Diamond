# coding=utf-8

"""
Collect data from S.M.A.R.T.'s attribute reporting.

#### Dependencies

 * [smartmontools](http://sourceforge.net/apps/trac/smartmontools/wiki)

"""

import diamond.collector
import subprocess
import re
import os
from diamond.collector import str_to_bool


class SmartCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(SmartCollector, self).get_default_config_help()
        config_help.update({
            'devices': "device regex to collect stats on",
            'bin':         'The path to the smartctl binary',
            'use_sudo':    'Use sudo?',
            'sudo_cmd':    'Path to sudo',
        })
        return config_help

    def get_default_config(self):
        """
        Returns default configuration options.
        """
        config = super(SmartCollector, self).get_default_config()
        config.update({
            'path': 'smart',
            'bin': 'smartctl',
            'use_sudo':         False,
            'sudo_cmd':         '/usr/bin/sudo',
            'devices': '^disk[0-9]$|^sd[a-z]$|^hd[a-z]$',
            'method': 'Threaded'
        })
        return config

    def collect(self):
        """
        Collect and publish S.M.A.R.T. attributes
        """
        devices = re.compile(self.config['devices'])

        for device in os.listdir('/dev'):
            if devices.match(device):

                command = [self.config['bin'], "-A", os.path.join('/dev',
                                                                  device)]

                if str_to_bool(self.config['use_sudo']):
                    command.insert(0, self.config['sudo_cmd'])

                attributes = subprocess.Popen(
                    command,
                    stdout=subprocess.PIPE
                ).communicate()[0].strip().splitlines()

                metrics = {}

                start_line = self.find_attr_start_line(attributes)
                for attr in attributes[start_line:]:
                    attribute = attr.split()
                    if attribute[1] != "Unknown_Attribute":
                        metric = "%s.%s" % (device, attribute[1])
                    else:
                        metric = "%s.%s" % (device, attribute[0])

                    # New metric? Store it
                    if metric not in metrics:
                        metrics[metric] = attribute[9]
                    # Duplicate metric? Only store if it has a larger value
                    # This happens semi-often with the Temperature_Celsius
                    # attribute You will have a PASS/FAIL after the real temp,
                    # so only overwrite if The earlier one was a
                    # PASS/FAIL (0/1)
                    elif metrics[metric] == 0 and attribute[9] > 0:
                        metrics[metric] = attribute[9]
                    else:
                        continue

                for metric in metrics.keys():
                    self.publish(metric, metrics[metric])

    def find_attr_start_line(self, lines, min_line=4, max_line=9):
        """
        Return line number of the first real attribute and value.
        The first line is 0.  If the 'ATTRIBUTE_NAME' header is not
        found, return the index after max_line.
        """
        for idx, line in enumerate(lines[min_line:max_line]):
            col = line.split()
            if len(col) > 1 and col[1] == 'ATTRIBUTE_NAME':
                return idx + min_line + 1

        self.log.warn('ATTRIBUTE_NAME not found in second column of'
                      ' smartctl output between lines %d and %d.'
                      % (min_line, max_line))

        return max_line + 1
