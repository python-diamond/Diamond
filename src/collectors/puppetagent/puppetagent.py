# coding=utf-8

"""
Collect stats from puppet agent's last_run_summary.yaml

#### Dependencies

 * yaml

"""

try:
    import yaml
except ImportError:
    yaml = None

import diamond.collector


class PuppetAgentCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(PuppetAgentCollector,
                            self).get_default_config_help()
        config_help.update({
            'yaml_path': "Path to last_run_summary.yaml",
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(PuppetAgentCollector, self).get_default_config()
        config.update({
            'yaml_path': '/var/lib/puppet/state/last_run_summary.yaml',
            'path':     'puppetagent',
        })
        return config

    def _get_summary(self):
        summary_fp = open(self.config['yaml_path'], 'r')

        try:
            summary = yaml.load(summary_fp)
        finally:
            summary_fp.close()

        return summary

    def collect(self):
        if yaml is None:
            self.log.error('Unable to import yaml')
            return

        summary = self._get_summary()

        for sect, data in summary.items():
            for stat, value in data.items():
                if value is None or isinstance(value, str):
                    continue

                metric = '.'.join([sect, stat])
                self.publish(metric, value)
