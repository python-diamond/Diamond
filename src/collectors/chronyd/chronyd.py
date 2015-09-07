# coding=utf-8

"""
Collect metrics from chrony - http://chrony.tuxfamily.org/

#### Dependencies

 * subprocess

"""

import re
import subprocess
import diamond.collector
import diamond.convertor
from diamond.collector import str_to_bool
LINE_PATTERN = re.compile(
    '^(?P<source>\S+).*\s+(?P<offset>[+-]\d+)(?P<unit>\w+)\s+')
IP_PATTERN = re.compile('^\d+\.\d+\.\d+\.\d+$')


def cleanup_source(source):
    if IP_PATTERN.search(source):
        return source.replace('.', '_')
    if '.' in source:
        hostname, _ = source.split('.', 1)
        return hostname
    return source


class ChronydCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(ChronydCollector, self).get_default_config_help()
        config_help.update({
            'bin':         'The path to the chronyc binary',
            'use_sudo':    'Use sudo?',
            'sudo_cmd':    'Path to sudo',
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(ChronydCollector, self).get_default_config()
        config.update({
            'path':             'chrony',
            'bin':              '/usr/bin/chronyc',
            'use_sudo':         False,
            'sudo_cmd':         '/usr/bin/sudo',
        })
        return config

    def get_output(self):
        try:
            command = [self.config['bin'], 'sourcestats']

            if str_to_bool(self.config['use_sudo']):
                command.insert(0, self.config['sudo_cmd'])

            return subprocess.Popen(command,
                                    stdout=subprocess.PIPE).communicate()[0]
        except OSError:
            return ""

    def collect(self):
        output = self.get_output()

        for line in output.strip().split("\n"):
            m = LINE_PATTERN.search(line)
            if m is None:
                continue

            source = cleanup_source(m.group('source'))
            offset = float(m.group('offset'))
            unit = m.group('unit')

            try:
                value = diamond.convertor.time.convert(offset, unit, 'ms')
            except NotImplementedError, e:
                self.log.error('Unable to convert %s%s: %s', offset, unit, e)
                continue

            self.publish('%s.offset_ms' % source, value)
