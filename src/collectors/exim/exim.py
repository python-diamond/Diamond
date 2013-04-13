# coding=utf-8

"""
Shells out to get the exim queue length

#### Dependencies

 * /usr/sbin/exim

"""

import diamond.collector
import subprocess
import os
from diamond.collector import str_to_bool


class EximCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(EximCollector, self).get_default_config_help()
        config_help.update({
            'bin':         'The path to the exim binary',
            'use_sudo':    'Use sudo?',
            'sudo_cmd':    'Path to sudo',
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(EximCollector, self).get_default_config()
        config.update({
            'path':            'exim',
            'method':          'threaded',
            'bin':              '/usr/sbin/exim',
            'use_sudo':         False,
            'sudo_cmd':         '/usr/bin/sudo',
        })
        return config

    def collect(self):
        if not os.access(self.config['bin'], os.X_OK):
            return

        command = [self.config['bin'], '-bpc']

        if str_to_bool(self.config['use_sudo']):
            command.insert(0, self.config['sudo_cmd'])

        queuesize = subprocess.Popen(
            command, stdout=subprocess.PIPE).communicate()[0].split()

        if not len(queuesize):
            return
        queuesize = queuesize[-1]
        self.publish('queuesize', queuesize)
