# coding=utf-8

"""
The MemoryCgroupCollector collects memory metric for cgroups

Stats that we are interested in tracking
cache - # of bytes of page cache memory.
rss   - # of bytes of anonymous and swap cache memory.
swap  - # of bytes of swap usage

#### Dependencies

/sys/fs/cgroup/memory/memory.stat
"""

import diamond.collector
import os

_KEY_MAPPING = [
    'cache',
    'rss',
    'swap'
]


class MemoryCgroupCollector(diamond.collector.Collector):
    MEMORY_PATH = '/sys/fs/cgroup/memory/'

    def get_default_config_help(self):
        config_help = super(
            MemoryCgroupCollector, self).get_default_config_help()
        config_help.update({
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(MemoryCgroupCollector, self).get_default_config()
        config.update({
            'path':     'memory_cgroup',
            'method':   'Threaded',
        })
        return config

    def collect(self):
        # find all memory.stat files
        matches = []
        for root, dirnames, filenames in os.walk(self.MEMORY_PATH):
            for filename in filenames:
                if filename == 'memory.stat':
                    # matches will contain a tuple contain path to cpuacct.stat
                    # and the parent of the stat
                    parent = root.replace(self.MEMORY_PATH,
                                          "").replace("/", ".")
                    if parent == '':
                        parent = 'system'
                    matches.append((parent, os.path.join(root, filename)))

        # Read metrics from cpuacct files
        results = {}
        for match in matches:
            results[match[0]] = {}
            stat_file = open(match[1])
            elements = [line.split() for line in stat_file]
            stat_file.close()

            for el in elements:
                name, value = el
                if name not in _KEY_MAPPING:
                    continue
                for unit in self.config['byte_unit']:
                    value = diamond.convertor.binary.convert(
                        value=value, oldUnit='B', newUnit=unit)
                    results[match[0]][name] = value
                    # TODO: We only support one unit node here. Fix it!
                    break

        # create metrics from collected utimes and stimes for cgroups
        for parent, cpuacct in results.iteritems():
            for key, value in cpuacct.iteritems():
                metric_name = '.'.join([parent, key])
                self.publish(metric_name, value, metric_type='GAUGE')
        return True
