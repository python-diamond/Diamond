# coding=utf-8

"""
Shells out to get the value of sysctl net.netfilter.nf_conntrack_count

#### Dependencies

 * /sbin/sysctl

"""

import diamond.collector
import subprocess
import os
import re
from diamond.collector import str_to_bool

_RE = re.compile(r'^([a-z\._]*) = ([0-9]*)$')


class ConnTrackCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(ConnTrackCollector, self).get_default_config_help()
        config_help.update({
            'use_sudo':    'Use sudo?',
            'sudo_cmd':    'Path to sudo',
            'bin':         'The path to the sysctl binary',
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(ConnTrackCollector, self).get_default_config()
        config.update({
            'path':             'conntrack',
            'use_sudo':         False,
            'sudo_cmd':         '/usr/bin/sudo',
            'bin':              '/sbin/sysctl',
        })
        return config

    def collect(self):
        if not os.access(self.config['bin'], os.X_OK):
            self.log.error("%s is not executable", self.config['bin'])
            return False

        command = [self.config['bin'], 'net.netfilter.nf_conntrack_count']

        if str_to_bool(self.config['use_sudo']):
            command.insert(0, self.config['sudo_cmd'])

        line = subprocess.Popen(command,
                                stdout=subprocess.PIPE).communicate()[0]

        match = _RE.match(line)
        if match:
            self.publish('nf_conntrack_count', int(match.group(2)))
