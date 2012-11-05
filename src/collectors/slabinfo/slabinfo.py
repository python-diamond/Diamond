# coding=utf-8

"""
The SlabInfoCollector collects metrics on process stats from
/proc/slabinfo

#### Dependencies

 * /proc/slabinfo

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


class SlabInfoCollector(diamond.collector.Collector):

    PROC = '/proc/slabinfo'

    def get_default_config_help(self):
        config_help = super(SlabInfoCollector, self).get_default_config_help()
        config_help.update({
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(SlabInfoCollector, self).get_default_config()
        config.update({
            'path':     'slabinfo'
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
            if line.startswith('slabinfo'):
                continue

            if line.startswith('#'):
                keys = line.split()[1:]
                continue

            data = line.split()

            for key in ['<active_objs>', '<num_objs>', '<objsize>',
                        '<objperslab>', '<pagesperslab>']:
                i = keys.index(key)
                metric_name = data[0] + '.' + key.replace(
                    '<', '').replace('>', '')
                metric_value = int(data[i])
                self.publish(metric_name, metric_value)

            for key in ['<limit>', '<batchcount>', '<sharedfactor>']:
                i = keys.index(key)
                metric_name = data[0] + '.tunables.' + key.replace(
                    '<', '').replace('>', '')
                metric_value = int(data[i])
                self.publish(metric_name, metric_value)

            for key in ['<active_slabs>', '<num_slabs>', '<sharedavail>']:
                i = keys.index(key)
                metric_name = data[0] + '.slabdata.' + key.replace(
                    '<', '').replace('>', '')
                metric_value = int(data[i])
                self.publish(metric_name, metric_value)

        #Close file
        file.close()
