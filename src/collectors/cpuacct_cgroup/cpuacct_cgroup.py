# coding=utf-8

"""
The CpuAcctCGroupCollector collects CPU Acct metric for cgroups

#### Dependencies

/sys/fs/cgroup/cpuacct/cpuacct.stat
"""

import diamond.collector
import os


class CpuAcctCgroupCollector(diamond.collector.Collector):
    CPUACCT_PATH = '/sys/fs/cgroup/cpuacct/'

    def get_default_config_help(self):
        config_help = super(
            CpuAcctCgroupCollector, self).get_default_config_help()
        config_help.update({
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(CpuAcctCgroupCollector, self).get_default_config()
        config.update({
            'path':     'cpuacct',
            'xenfix':   None,
        })
        return config

    def collect(self):
        # find all cpuacct.stat files
        matches = []
        for root, dirnames, filenames in os.walk(self.CPUACCT_PATH):
            for filename in filenames:
                if filename == 'cpuacct.stat':
                    # matches will contain a tuple contain path to cpuacct.stat
                    # and the parent of the stat
                    parent = root.replace(self.CPUACCT_PATH,
                                          "").replace("/", ".")
                    if parent == '':
                        parent = 'system'
                    matches.append((parent, os.path.join(root, filename)))

        # Read utime and stime from cpuacct files
        results = {}
        for match in matches:
            results[match[0]] = {}
            stat_file = open(match[1])
            elements = [line.split() for line in stat_file]
            for el in elements:
                results[match[0]][el[0]] = el[1]
                stat_file.close()

        # create metrics from collected utimes and stimes for cgroups
        for parent, cpuacct in results.iteritems():
            for key, value in cpuacct.iteritems():
                metric_name = '.'.join([parent, key])
                self.publish(metric_name, value, metric_type='GAUGE')
        return True
