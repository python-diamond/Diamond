# coding=utf-8

"""
Shells out to get ossec statistics, which may or may not require sudo access.

Metrics:
- agents.active
- agents.never_connected
- agents.disconnected
- agents.active_local

#### Dependencies

 * /var/ossec/bin/agent_control

"""

import diamond.collector
from diamond.collector import str_to_bool
import subprocess
import re


class OssecCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(OssecCollector, self).get_default_config_help()
        config_help.update({
            'bin': 'Path to agent_control binary',
            'use_sudo': 'Use sudo?',
            'sudo_cmd': 'Path to sudo',
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(OssecCollector, self).get_default_config()
        config.update({
            'bin':              '/var/ossec/bin/agent_control',
            'use_sudo':         True,
            'sudo_cmd':         '/usr/bin/sudo',
            'path':             'ossec',
        })
        return config

    def collect(self):
        command = [self.config['bin'], '-l']

        if str_to_bool(self.config['use_sudo']):
            command.insert(0, self.config['sudo_cmd'])

        try:
            p = subprocess.Popen(command, stdout=subprocess.PIPE)
            res = p.communicate()[0]
        except Exception, e:
            self.log.error('Unable to exec cmd: %s, because %s'
                           % (' '.join(command), str(e)))
            return

        if res == '':
            self.log.error('Empty result from exec cmd: %s'
                           % (' '.join(command)))
            return

        states = {}
        for line in res.split("\n"):
            #    ID: 000, Name: local-ossec-001.localdomain (server), IP:\
            # 127.0.0.1, Active/Local
            if not line.startswith('   ID: '):
                continue
            fragments = line.split(',')
            state = fragments[-1].lstrip()
            if state not in states:
                states[state] = 1
            else:
                states[state] += 1

        for state, count in states.items():
            name = 'agents.' + re.sub('[^a-z]', '_', state.lower())
            self.publish(name, count)
