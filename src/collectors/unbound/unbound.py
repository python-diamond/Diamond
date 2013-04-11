# coding=utf-8

"""
Collect stats from the unbound resolver

#### Dependencies

    * subprocess
    * collections.defaultdict or kitchen

"""

import subprocess

try:
    from collections import defaultdict
    defaultdict  # Pyflakes
except ImportError:
    from kitchen.pycompat25.collections import defaultdict

import diamond.collector
from diamond.collector import str_to_bool


class UnboundCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(UnboundCollector, self).get_default_config_help()
        config_help.update({
            'bin':          'Path to unbound-control binary',
            'use_sudo':     'Use sudo?',
            'sudo_cmd':     'Path to sudo',
            'histogram':    'Include histogram in collection',
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(UnboundCollector, self).get_default_config()
        config.update({
            'path':         'unbound',
            'bin':          '/usr/sbin/unbound-control',
            'use_sudo':     False,
            'sudo_cmd':     '/usr/bin/sudo',
            'histogram':    True,
        })
        return config

    def get_unbound_control_output(self):
        try:
            command = [self.config['bin'] + ' stats']

            if str_to_bool(self.config['use_sudo']):
                command.insert(0, self.config['sudo_cmd'])

            return subprocess.Popen(command,
                                    stdout=subprocess.PIPE,
                                    shell=True).communicate()[0]
        except OSError:
            self.log.exception("Unable to run %s", command)
            return ""

    def get_massaged_histogram(self, raw_histogram):
        histogram = defaultdict(int)

        for intv in sorted(raw_histogram.keys()):
            if intv <= 0.001024:
                # Let's compress <1ms into 1 data point
                histogram['1ms'] += raw_histogram[intv]
            elif intv < 1.0:
                # Convert to ms and since we're using the upper limit
                # divide by 2 for lower limit
                intv_name = ''.join([str(int(intv / 0.001024 / 2)), 'ms+'])
                histogram[intv_name] = raw_histogram[intv]
            elif intv == 1.0:
                histogram['512ms+'] = raw_histogram[intv]
            elif intv > 1.0 and intv <= 64.0:
                # Convert upper limit into lower limit seconds
                intv_name = ''.join([str(int(intv / 2)), 's+'])
                histogram[intv_name] = raw_histogram[intv]
            else:
                # Compress everything >64s into 1 data point
                histogram['64s+'] += raw_histogram[intv]

        return histogram

    def collect(self):
        stats_output = self.get_unbound_control_output()

        raw_histogram = {}

        for line in stats_output.splitlines():
            stat_name, stat_value = line.split('=')

            if not stat_name.startswith('histogram'):
                self.publish(stat_name, stat_value)
            elif self.config['histogram']:
                hist_intv = float(stat_name.split('.', 4)[4])
                raw_histogram[hist_intv] = float(stat_value)

        if self.config['histogram']:
            histogram = self.get_massaged_histogram(raw_histogram)

            for intv, value in histogram.iteritems():
                self.publish('histogram.' + intv, value)
