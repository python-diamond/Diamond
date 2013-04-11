# coding=utf-8

"""
Collect the emails in the postfix queue

#### Dependencies

 * subprocess

"""

import subprocess
import diamond.collector
from diamond.collector import str_to_bool


class PostqueueCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(PostqueueCollector, self).get_default_config_help()
        config_help.update({
            'bin':         'The path to the postqueue binary',
            'use_sudo':    'Use sudo?',
            'sudo_cmd':    'Path to sudo',
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(PostqueueCollector, self).get_default_config()
        config.update({
            'path':             'postqueue',
            'bin':              '/usr/bin/postqueue',
            'use_sudo':         False,
            'sudo_cmd':         '/usr/bin/sudo',
        })
        return config

    def get_postqueue_output(self):
        try:
            command = [self.config['bin'], '-p']

            if str_to_bool(self.config['use_sudo']):
                command.insert(0, self.config['sudo_cmd'])

            return subprocess.Popen(command,
                                    stdout=subprocess.PIPE).communicate()[0]
        except OSError:
            return ""

    def collect(self):
        output = self.get_postqueue_output()

        try:
            postqueue_count = int(output.strip().split("\n")[-1].split()[-2])
        except:
            postqueue_count = 0

        self.publish('count', postqueue_count)
