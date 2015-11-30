# coding=utf-8

"""
Collect disk temperature with S.M.A.R.T.

This collector use hddtemp to collect only the disk temperature from the disk
S.M.A.R.T information. This can be faster than smartctl since it only extracts
a single value.

#### Dependencies

 * [hddtemp](http://www.guzu.net/linux/hddtemp.php)

"""

import os
import re
import subprocess

import diamond.collector
from diamond.collector import str_to_bool


class DiskTemperatureCollector(diamond.collector.Collector):

    def process_config(self):
        super(DiskTemperatureCollector, self).process_config()
        self.devices = re.compile(self.config['devices'])

    def get_default_config_help(self):
        config_help = super(DiskTemperatureCollector,
                            self).get_default_config_help()
        config_help.update({
            'devices': "device regex to collect stats on",
            'bin':         'The path to the hddtemp binary',
            'use_sudo':    'Use sudo?',
            'sudo_cmd':    'Path to sudo',
        })
        return config_help

    def get_default_config(self):
        """
        Returns default configuration options.
        """
        config = super(DiskTemperatureCollector, self).get_default_config()
        config.update({
            'path': 'disktemp',
            'bin': 'hddtemp',
            'use_sudo': False,
            'sudo_cmd': '/usr/bin/sudo',
            'devices': '^disk[0-9]$|^sd[a-z]$|^hd[a-z]$'
        })
        return config

    def get_temp(self, device):
        command = [self.config['bin'], '-n', device]

        if str_to_bool(self.config['use_sudo']):
            command.insert(0, self.config['sudo_cmd'])

        return subprocess.Popen(command, stdout=subprocess.PIPE)

    def match_device(self, device, path):
        m = self.devices.match(device)
        if m:
            key = device
            # If the regex has a capture group for pretty printing, pick
            # the last matched capture group
            if self.devices.groups > 0:
                key = '.'.join(filter(None, [g for g in m.groups()]))

            return {key: self.get_temp(os.path.join('/dev', device))}

        return {}

    def collect(self):
        """
        Collect and publish disk temperatures
        """
        instances = {}

        # Support disks such as /dev/(sd.*)
        for device in os.listdir('/dev/'):
            instances.update(self.match_device(device, '/dev/'))

        # Support disk by id such as /dev/disk/by-id/wwn-(.*)
        for device_id in os.listdir('/dev/disk/by-id/'):
            instances.update(self.match_device(device, '/dev/disk/by-id/'))

        metrics = {}
        for device, p in instances.items():
            output = p.communicate()[0].strip()

            try:
                metrics[device + ".Temperature"] = float(output)
            except:
                self.log.warn('Disk temperature retrieval failed on ' + device)

        for metric in metrics.keys():
            self.publish(metric, metrics[metric])
