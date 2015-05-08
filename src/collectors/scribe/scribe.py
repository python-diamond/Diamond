# coding=utf-8

"""
Collect counters from scribe

#### Dependencies

    * /usr/sbin/scribe_ctrl, distributed with scribe

"""

import subprocess
import string

import diamond.collector


class ScribeCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(ScribeCollector, self).get_default_config_help()
        config_help.update({
            'scribe_ctrl_bin': 'Path to scribe_ctrl binary',
            'scribe_port': 'Scribe port',
        })
        return config_help

    def get_default_config(self):
        config = super(ScribeCollector, self).get_default_config()
        config.update({
            'path': 'scribe',
            'scribe_ctrl_bin': self.find_binary('/usr/sbin/scribe_ctrl'),
            'scribe_port': None,
        })
        return config

    def key_to_metric(self, key):
        """Replace all non-letter characters with underscores"""
        return ''.join(l if l in string.letters else '_' for l in key)

    def get_scribe_ctrl_output(self):
        cmd = [self.config['scribe_ctrl_bin'], 'counters']

        if self.config['scribe_port'] is not None:
            cmd.append(self.config['scribe_port'])

        self.log.debug("Running command %r", cmd)

        try:
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
        except OSError:
            self.log.exception("Unable to run %r", cmd)
            return ""

        stdout, stderr = p.communicate()

        if p.wait() != 0:
            self.log.warning("Command failed %r", cmd)
            self.log.warning(stderr)

        return stdout

    def get_scribe_stats(self):
        output = self.get_scribe_ctrl_output()

        data = {}

        for line in output.splitlines():
            key, val = line.rsplit(':', 1)
            metric = self.key_to_metric(key)
            data[metric] = int(val)

        return data.items()

    def collect(self):
        for stat, val in self.get_scribe_stats():
            self.publish(stat, val)
