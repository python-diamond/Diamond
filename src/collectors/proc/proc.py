# coding=utf-8

"""
The ProcessStatCollector collects metrics on process stats from
/proc/stat

#### Dependencies

 * /proc/stat

"""

import platform
import os
import diamond.collector

# Detect the architecture of the system
# and set the counters for MAX_VALUES
# appropriately. Otherwise, rolling over
# counters will cause incorrect or
# negative values.
if platform.architecture()[0] == '64bit':
    counter = (2 ** 64) - 1
else:
    counter = (2 ** 32) - 1


class ProcessStatCollector(diamond.collector.Collector):

    PROC = '/proc/stat'

    def get_default_config_help(self):
        config_help = super(ProcessStatCollector,
                            self).get_default_config_help()
        config_help.update({
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(ProcessStatCollector, self).get_default_config()
        config.update({
            'path':     'proc'
        })
        return config

    def collect(self):
        """
        Collect process stat data
        """
        if not os.access(self.PROC, os.R_OK):
            return False

        #Open PROC file
        file = open(self.PROC, 'r')

        #Get data
        for line in file:

            if line.startswith('ctxt') or line.startswith('processes'):
                data = line.split()
                metric_name = data[0]
                metric_value = int(data[1])
                metric_value = int(self.derivative(metric_name,
                                                   long(metric_value),
                                                   counter))
                self.publish(metric_name, metric_value)

            if line.startswith('procs_') or line.startswith('btime'):
                data = line.split()
                metric_name = data[0]
                metric_value = int(data[1])
                self.publish(metric_name, metric_value)

        #Close file
        file.close()
