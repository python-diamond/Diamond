# coding=utf-8

"""
This class collects data from NUT, a UPS interface for linux.

#### Dependencies

 * nut/upsc to be installed, configured and running.

"""

import diamond.collector
import os
import subprocess
from diamond.collector import str_to_bool


class UPSCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(UPSCollector, self).get_default_config_help()
        config_help.update({
            'ups_name':    'The name of the ups to collect data for',
            'bin':         'The path to the upsc binary',
            'use_sudo':    'Use sudo?',
            'sudo_cmd':    'Path to sudo',
        })
        return config_help

    def get_default_config(self):
        """
        Returns default collector settings.
        """

        config = super(UPSCollector, self).get_default_config()
        config.update({
            'path':             'ups',
            'ups_name':         'cyberpower',
            'bin':              '/bin/upsc',
            'use_sudo':         False,
            'sudo_cmd':         '/usr/bin/sudo',
        })
        return config

    def collect(self):
        if not os.access(self.config['bin'], os.X_OK):
            self.log.error("%s is not executable", self.config['bin'])
            return False

        command = [self.config['bin'], self.config['ups_name']]

        if str_to_bool(self.config['use_sudo']):
            command.insert(0, self.config['sudo_cmd'])

        p = subprocess.Popen(command,
                             stdout=subprocess.PIPE).communicate()[0]

        for ln in p.strip().splitlines():
            datapoint = ln.split(": ")

            try:
                val = float(datapoint[1])
            except:
                continue

            if len(datapoint[0].split(".")) == 2:
                # If the metric name is the same as the subfolder
                # double it so it's visible.
                name = ".".join([datapoint[0], datapoint[0].split(".")[1]])
            else:
                name = datapoint[0]

            self.publish(name, val)
