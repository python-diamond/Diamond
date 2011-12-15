# Copyright (C) 2011 by Rob Smith
# http://www.kormoc.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import platform

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
    """
    The InterruptCollector class collects metrics on interrupts from
    /proc/interrupts
    """
    PROC='/proc/interrupts'

    def collect(self):
        """
        Collect interrupt data
        """
        #Open PROC file
        file=open(self.PROC,'r')
        #Get data
        cpuCount = None
        for line in file:
            if not cpuCount:
                cpuCount = len(line.split())
            else:
                data = line.strip().split(None, cpuCount+2)
                data[0] = data[0].replace(':', '');

                if len(data) == 2:
                    metric_name = data[0]
                    metric_value = data[1]
                    self.publish(metric_name, self.derivative(metric_name, long(metric_value), counter))
                else:
                    if len(data[0]) == 3:
                        metric_name = ((data[len(data)-2]+' '+data[len(data)-1]).replace(' ','_'))+'.'
                    else:
                        metric_name = ((data[len(data)-2]).replace(' ','_'))+'.'+((data[len(data)-1]).replace(', ', '-').replace(' ','_'))+'.'+data[0]+'.'
                    total = 0
                    for index, value in enumerate(data):
                        if index == 0 or index >= cpuCount+1:
                            continue

                        metric_name_node = metric_name+'CPU'+str(index-1)
                        value = int(self.derivative(metric_name_node, long(value), counter))
                        total += value
                        self.publish(metric_name_node, value)

                    # Roll up value
                    metric_name_node = metric_name+'total'
                    self.publish(metric_name_node, total)

        #Close file
        file.close()
