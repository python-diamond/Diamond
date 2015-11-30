# coding=utf-8

"""
Collector that reports amavis metrics as reported by amavisd-agent

#### Dependencies

* amavisd-agent must be present in PATH

"""

import os
import subprocess
import re

import diamond.collector
import diamond.convertor
from diamond.collector import str_to_bool


class AmavisCollector(diamond.collector.Collector):
    # From the source of amavisd-agent and it seems like the three interesting
    # formats are these:  ("x y/h", "xMB yMB/h", "x s y s/msg"),
    # so this, ugly as it is to hardcode it this way, it should be right.
    #
    # The other option would be to directly read and decode amavis' berkeley
    # db, and I don't even want to get there

    matchers = [
        re.compile(r'^\s*(?P<name>sysUpTime)\s+TimeTicks\s+(?P<time>\d+)\s+'
                   r'\([\w:\., ]+\)\s*$'),
        re.compile(r'^\s*(?P<name>[\w]+)\s+(?P<time>[\d]+) s\s+'
                   r'(?P<frequency>[\d.]+) s/msg\s+\([\w]+\)\s*$'),
        re.compile(r'^\s*(?P<name>[\w.-]+)\s+(?P<count>[\d]+)\s+'
                   r'(?P<frequency>[\d.]+)/h\s+(?P<percentage>[\d.]+) %'
                   r'\s\([\w]+\)\s*$'),
        re.compile(r'^\s*(?P<name>[\w.-]+)\s+(?P<size>[\d]+)MB\s+'
                   r'(?P<frequency>[\d.]+)MB/h\s+(?P<percentage>[\d.]+) %'
                   r'\s\([\w]+\)\s*$'),
    ]

    def get_default_config_help(self):
        config_help = super(AmavisCollector, self).get_default_config_help()
        config_help.update({
            'amavisd_exe': 'The path to amavisd-agent',
            'use_sudo': 'Call amavisd-agent using sudo',
            'sudo_exe': 'The path to sudo',
            'sudo_user': 'The user to use if using sudo',
        })
        return config_help

    def get_default_config(self):
        config = super(AmavisCollector, self).get_default_config()
        config.update({
            'path': 'amavis',
            'amavisd_exe': '/usr/sbin/amavisd-agent',
            'use_sudo': False,
            'sudo_exe': '/usr/bin/sudo',
            'sudo_user': 'amavis',
        })
        return config

    def collect(self):
        """
        Collect memory stats
        """
        try:
            if str_to_bool(self.config['use_sudo']):
                # Use -u instead of --user as the former is more portable. Not
                # all versions of sudo support the long form --user.
                cmdline = [
                    self.config['sudo_exe'], '-u', self.config['sudo_user'],
                    '--', self.config['amavisd_exe'], '-c', '1'
                ]
            else:
                cmdline = [self.config['amavisd_exe'], '-c', '1']
            agent = subprocess.Popen(cmdline, stdout=subprocess.PIPE)
            agent_out = agent.communicate()[0]
            lines = agent_out.strip().split(os.linesep)
            for line in lines:
                for rex in self.matchers:
                    res = rex.match(line)
                    if res:
                        groups = res.groupdict()
                        name = groups['name']
                        for metric, value in groups.items():
                            if metric == 'name':
                                continue
                            mtype = 'GAUGE'
                            if metric in ('count', 'time'):
                                mtype = 'COUNTER'
                            self.publish("{0}.{1}".format(name, metric),
                                         value, metric_type=mtype)

        except OSError as err:
            self.log.error("Could not run %s: %s",
                           self.config['amavisd_exe'],
                           err)
            return None

        return True
