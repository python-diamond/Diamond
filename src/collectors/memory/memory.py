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

from decimal import Decimal

try:
    import psutil
    psutil  # workaround for pyflakes issue #13
except ImportError:
    psutil = None

_KEY_MAPPING = [
    'MemTotal',
    'MemFree',
    'MemAvailable',  # needs kernel 3.14
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
            'path': 'memory',
            'method': 'Threaded',
            'force_psutil': 'False'
            # Collect all the nodes or just a few standard ones?
            # Uncomment to enable
            # 'detailed': 'True'
        })
        return config

    def collect(self):
        """
        Collect memory stats
        """
        if ((os.access(self.PROC, os.R_OK) and
             self.config.get('force_psutil') != 'True')):
            file = open(self.PROC)
            data = file.read()
            file.close()

            memory_total = None
            memory_available = None
            for line in data.splitlines():
                try:
                    name, value, units = line.split()
                    name = name.rstrip(':')
                    value = int(value)

                    if ((name not in _KEY_MAPPING and
                         'detailed' not in self.config)):
                        continue

                    if name in 'MemTotal':
                        memory_total = value
                    elif name in 'MemAvailable':
                        memory_available = value

                    for unit in self.config['byte_unit']:
                        value = diamond.convertor.binary.convert(value=value,
                                                                 oldUnit=units,
                                                                 newUnit=unit)
                        self.publish(name, value, metric_type='GAUGE')

                        # TODO: We only support one unit node here. Fix it!
                        break

                except ValueError:
                    continue

            if memory_total is not None and memory_available is not None:
                memory_used = memory_total - memory_available
                memory_used_percent = Decimal(str(100.0 *
                                              memory_used /
                                              memory_total))
                self.publish('MemUsedPercentage',
                             round(memory_used_percent, 2),
                             metric_type='GAUGE')
            return True
        else:
            if not psutil:
                self.log.error('Unable to import psutil')
                self.log.error('No memory metrics retrieved')
                return None

            # psutil.phymem_usage() and psutil.virtmem_usage() are deprecated.
            if hasattr(psutil, "phymem_usage"):
                phymem_usage = psutil.phymem_usage()
                virtmem_usage = psutil.virtmem_usage()
            else:
                phymem_usage = psutil.virtual_memory()
                virtmem_usage = psutil.swap_memory()

            units = 'B'

            for unit in self.config['byte_unit']:
                memory_total = value = diamond.convertor.binary.convert(
                    value=phymem_usage.total, oldUnit=units, newUnit=unit)
                self.publish('MemTotal', value, metric_type='GAUGE')

                memory_available = value = diamond.convertor.binary.convert(
                    value=phymem_usage.available, oldUnit=units, newUnit=unit)
                self.publish('MemAvailable', value, metric_type='GAUGE')

                memory_used = memory_total - memory_available

                memory_used_percent = Decimal(str(100.0 *
                                              memory_used /
                                              memory_total))
                self.publish('MemUsedPercentage',
                             round(memory_used_percent, 2),
                             metric_type='GAUGE')

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
