# coding=utf-8

"""
Collect stats from ntpd

#### Dependencies

    * subprocess

"""

import subprocess

import diamond.collector
from diamond.collector import str_to_bool


class NtpdCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(NtpdCollector, self).get_default_config_help()
        config_help.update({
            'ntpq_bin':     'Path to ntpq binary',
            'ntpdc_bin':    'Path to ntpdc binary',
            'use_sudo':     'Use sudo?',
            'sudo_cmd':     'Path to sudo',
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(NtpdCollector, self).get_default_config()
        config.update({
            'path':         'ntpd',
            'ntpq_bin':     '/usr/bin/ntpq',
            'ntpdc_bin':    '/usr/bin/ntpdc',
            'use_sudo':     False,
            'sudo_cmd':     '/usr/bin/sudo',
        })
        return config

    def run_command(self, command):
        try:
            if str_to_bool(self.config['use_sudo']):
                command.insert(0, self.config['sudo_cmd'])

            return subprocess.Popen(command,
                                    stdout=subprocess.PIPE).communicate()[0]
        except OSError:
            self.log.exception("Unable to run %s", command)
            return ""

    def get_ntpq_output(self):
        return self.run_command([self.config['ntpq_bin'], '-np'])

    def get_ntpq_stats(self):
        output = self.get_ntpq_output()

        data = {}

        for line in output.splitlines():
            # Only care about system peer
            if not line.startswith('*'):
                continue

            parts = line[1:].split()

            data['stratum'] = parts[2]
            data['when'] = parts[4]
            data['poll'] = parts[5]
            data['reach'] = parts[6]
            data['delay'] = parts[7]
            data['jitter'] = parts[9]

        return data.items()

    def get_ntpdc_output(self):
        return self.run_command([self.config['ntpdc_bin'], '-c', 'kerninfo'])

    def get_ntpdc_stats(self):
        output = self.get_ntpdc_output()

        data = {}

        for line in output.splitlines():
            key, val = line.split(':')
            val = float(val.split()[0])

            if key == 'pll offset':
                data['offset'] = val
            elif key == 'pll frequency':
                data['frequency'] = val
            elif key == 'maximum error':
                data['max_error'] = val
            elif key == 'estimated error':
                data['est_error'] = val

        return data.items()

    def collect(self):
        for stat, val in self.get_ntpq_stats():
            self.publish(stat, val)

        for stat, val in self.get_ntpdc_stats():
            self.publish(stat, val)
