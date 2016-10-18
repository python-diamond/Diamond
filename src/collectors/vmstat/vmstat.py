# coding=utf-8

"""
Uses /proc/vmstat to collect data on virtual memory manager

#### Dependencies

 * /proc/vmstat

"""

import diamond.collector
import os
import re


class VMStatCollector(diamond.collector.Collector):

    PROC = '/proc/vmstat'
    MAX_VALUES = {
        'pgfault': diamond.collector.MAX_COUNTER,
        'pgmajfault': diamond.collector.MAX_COUNTER,
        'pgpgin': diamond.collector.MAX_COUNTER,
        'pgpgout': diamond.collector.MAX_COUNTER,
        'pswpin': diamond.collector.MAX_COUNTER,
        'pswpout': diamond.collector.MAX_COUNTER,
    }

    def get_default_config_help(self):
        config_help = super(VMStatCollector, self).get_default_config_help()
        config_help.update({
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(VMStatCollector, self).get_default_config()
        config.update({
            'path':     'vmstat'
        })
        return config

    def collect(self):
        if not os.access(self.PROC, os.R_OK):
            return None

        # open file
        file = open(self.PROC)
        exp = '^(pgfault|pgmajfault|pgpgin|pgpgout|pswpin|pswpout)\s(\d+)'
        reg = re.compile(exp)
        # Build regex
        for line in file:
            match = reg.match(line)
            if match:
                name = match.group(1)
                value = match.group(2)
                max_value = self.MAX_VALUES[name]
                derived = self.derivative(name, int(value), max_value)
                self.publish(name, derived, raw_value=int(value), precision=2)

        # Close file
        file.close()
