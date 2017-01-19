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
            'ntpq_bin':     self.find_binary('/usr/bin/ntpq'),
            'ntpdc_bin':    self.find_binary('/usr/bin/ntpdc'),
            'use_sudo':     False,
            'sudo_cmd':     self.find_binary('/usr/bin/sudo'),
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

            data['stratum'] = {'val': parts[2], 'precision': 0}
            data['when'] = {'val': parts[4], 'precision': 0}
            if data['when']['val'] == '-':
                # sometimes, ntpq returns value '-' for 'when', continuos
                # and try other system peer
                continue
            data['poll'] = {'val': parts[5], 'precision': 0}
            data['reach'] = {'val': parts[6], 'precision': 0}
            data['delay'] = {'val': parts[7], 'precision': 6}
            data['jitter'] = {'val': parts[9], 'precision': 6}

        def convert_to_second(when_ntpd_ouput):
            value = float(when_ntpd_ouput[:-1])
            if when_ntpd_ouput.endswith('m'):
                return value * 60
            elif when_ntpd_ouput.endswith('h'):
                return value * 3600
            elif when_ntpd_ouput.endswith('d'):
                return value * 86400

        if 'when' in data:
            if data['when']['val'] == '-':
                self.log.warning('ntpq returned bad value for "when"')
                return []

            if data['when']['val'].endswith(('m', 'h', 'd')):
                data['when']['val'] = convert_to_second(data['when']['val'])

        return data.items()

    def get_ntpdc_kerninfo_output(self):
        return self.run_command([self.config['ntpdc_bin'], '-c', 'kerninfo'])

    def get_ntpdc_kerninfo_stats(self):
        output = self.get_ntpdc_kerninfo_output()

        data = {}

        for line in output.splitlines():
            key, val = line.split(':')
            val = float(val.split()[0])

            if key == 'pll offset':
                data['offset'] = {'val': val, 'precision': 10}
            elif key == 'pll frequency':
                data['frequency'] = {'val': val, 'precision': 6}
            elif key == 'maximum error':
                data['max_error'] = {'val': val, 'precision': 6}
            elif key == 'estimated error':
                data['est_error'] = {'val': val, 'precision': 6}
            elif key == 'status':
                data['status'] = {'val': val, 'precision': 0}

        return data.items()

    def get_ntpdc_sysinfo_output(self):
        return self.run_command([self.config['ntpdc_bin'], '-c', 'sysinfo'])

    def get_ntpdc_sysinfo_stats(self):
        output = self.get_ntpdc_sysinfo_output()

        data = {}

        for line in output.splitlines():
            key, val = line.split(':')[0:2]
            try:
                val = float(val.split()[0])

                if key == 'root distance':
                    data['root_distance'] = {'val': val, 'precision': 6}
                elif key == 'root dispersion':
                    data['root_dispersion'] = {'val': val, 'precision': 6}
            except Exception:
                pass

        return data.items()

    def collect(self):
        for stat, v in self.get_ntpq_stats():
            self.publish(stat, v['val'], precision=v['precision'])

        for stat, v in self.get_ntpdc_kerninfo_stats():
            self.publish(stat, v['val'], precision=v['precision'])

        for stat, v in self.get_ntpdc_sysinfo_stats():
            self.publish(stat, v['val'], precision=v['precision'])
