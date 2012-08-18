# coding=utf-8

"""
The InterruptCollector class collects metrics on interrupts from
/proc/interrupts

#### Dependencies

 * /proc/interrupts

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


class InterruptCollector(diamond.collector.Collector):

    PROC = '/proc/interrupts'

    def get_default_config_help(self):
        config_help = super(InterruptCollector, self).get_default_config_help()
        config_help.update({
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(InterruptCollector, self).get_default_config()
        config.update({
            'path':     'interrupts'
        })
        return config

    def collect(self):
        """
        Collect interrupt data
        """
        if not os.access(self.PROC, os.R_OK):
            return False

        #Open PROC file
        file = open(self.PROC, 'r')
        #Get data
        cpuCount = None
        for line in file:
            if not cpuCount:
                cpuCount = len(line.split())
            else:
                data = line.strip().split(None, cpuCount + 2)
                data[0] = data[0].replace(':', '')

                if len(data) == 2:
                    metric_name = data[0]
                    metric_value = data[1]
                    self.publish(metric_name,
                                 self.derivative(metric_name,
                                                 long(metric_value),
                                                 counter))
                else:
                    if len(data[0]) == cpuCount + 1:
                        metric_name = data[0] + '.'
                    elif len(data[0]) == 3:
                        metric_name = (((data[-2] + ' '
                                         + data[-1]).replace(' ', '_')) + '.')
                    else:
                        metric_name = (((data[-2]).replace(' ', '_'))
                                       + '.'
                                       + ((data[-1]).replace(', ',
                                                             '-'
                                                             ).replace(' ',
                                                                       '_'))
                                       + '.' + data[0] + '.')
                    total = 0
                    for index, value in enumerate(data):
                        if index == 0 or index >= cpuCount + 1:
                            continue

                        metric_name_node = metric_name + 'CPU' + str(index - 1)
                        value = int(self.derivative(metric_name_node,
                                                    long(value), counter))
                        total += value
                        self.publish(metric_name_node, value)

                    # Roll up value
                    metric_name_node = metric_name + 'total'
                    self.publish(metric_name_node, total)

        #Close file
        file.close()
