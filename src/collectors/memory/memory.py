# coding=utf-8

"""
This class collects data on memory utilization

Note that MemFree may report no memory free. This may not actually be the case,
as memory is allocated to Buffers and Cache as well. See
[this link](http://www.linuxatemyram.com/) for more details.

#### Dependencies

* /proc/meminfo or psutil

"""

import diamond.collector
import diamond.convertor
import os

try:
    import psutil
except ImportError:
    psutil = None

_KEY_MAPPING = [
    'MemTotal',
    'MemFree',
    'Buffers',
    'Cached',
    'Active',
    'Dirty',
    'Inactive',
    'Shmem',
    'SwapTotal',
    'SwapFree',
    'SwapCached',
    'VmallocTotal',
    'VmallocUsed',
    'VmallocChunk',
    'Committed_AS',
]


class MemoryCollector(diamond.collector.Collector):

    PROC = '/proc/meminfo'

    def get_default_config_help(self):
        config_help = super(MemoryCollector, self).get_default_config_help()
        config_help.update({
            'detailed': 'Set to True to Collect all the nodes',
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(MemoryCollector, self).get_default_config()
        config.update({
            'path':     'memory',
            # Collect all the nodes or just a few standard ones?
            # Uncomment to enable
            #'detailed': 'True'
        })
        return config

    def collect(self):
        """
        Collect memory stats
        """
        if os.access(self.PROC, os.R_OK):
            file = open(self.PROC)
            data = file.read()
            file.close()

            for line in data.splitlines():
                try:
                    name, value, units = line.split()
                    name = name.rstrip(':')
                    value = int(value)

                    if (name not in _KEY_MAPPING
                            and 'detailed' not in self.config):
                        continue

                    for unit in self.config['byte_unit']:
                        value = diamond.convertor.binary.convert(value=value,
                                                                 oldUnit=units,
                                                                 newUnit=unit)
                        self.publish(name, value, metric_type='GAUGE')

                        # TODO: We only support one unit node here. Fix it!
                        break

                except ValueError:
                    continue
            return True
        else:
            if not psutil:
                self.log.error('Unable to import psutil')
                self.log.error('No memory metrics retrieved')
                return None

            phymem_usage = psutil.phymem_usage()
            virtmem_usage = psutil.virtmem_usage()
            units = 'B'

            for unit in self.config['byte_unit']:
                value = diamond.convertor.binary.convert(
                    value=phymem_usage.total, oldUnit=units, newUnit=unit)
                self.publish('MemTotal', value, metric_type='GAUGE')

                value = diamond.convertor.binary.convert(
                    value=phymem_usage.free, oldUnit=units, newUnit=unit)
                self.publish('MemFree', value, metric_type='GAUGE')

                value = diamond.convertor.binary.convert(
                    value=virtmem_usage.total, oldUnit=units, newUnit=unit)
                self.publish('SwapTotal', value, metric_type='GAUGE')

                value = diamond.convertor.binary.convert(
                    value=virtmem_usage.free, oldUnit=units, newUnit=unit)
                self.publish('SwapFree', value, metric_type='GAUGE')

                # TODO: We only support one unit node here. Fix it!
                break

            return True

        return None
