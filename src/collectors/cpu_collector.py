# Copyright (C) 2011-2012 by Ivan Pouzyrevsky.
# Copyright (C) 2010-2011 by Brightcove Inc. 
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

from diamond import *
import diamond.collector

class CPUCollector(diamond.collector.Collector):
    """
    The CPUCollector collects CPU utilization metric using /proc/stat.
    """

    PROC = '/proc/stat'
    MAX_VALUES = {
        'user': diamond.collector.MAX_COUNTER,
        'nice': diamond.collector.MAX_COUNTER,
        'system': diamond.collector.MAX_COUNTER,
        'idle': diamond.collector.MAX_COUNTER,
        'iowait': diamond.collector.MAX_COUNTER,
    }

    def collect(self):
        """
        Collector cpu stats
        """
        results = {}
        # Open file
        file = open(self.PROC)
        # Build Regex
        exp = '^(cpu[0-9]*)\s+(?P<user>\d+)\s+(?P<nice>\d+)\s+(?P<system>\d+)\s+(?P<idle>\d+)\s+(?P<iowait>\d+).*$'
        reg = re.compile(exp)
        for line in file:
            match = reg.match(line)

            if match:
                cpu = match.group(1)
                if cpu == 'cpu':
                    cpu = 'total'
                results[cpu] = {}
                results[cpu] = match.groupdict()
        # Close File
        file.close()
        
        for cpu in results.keys():
            stats = results[cpu]
            for s in stats.keys():
                # Get Metric Name 
                metric_name = '.'.join([cpu, s])
                # Publish Metric Derivative
                self.publish(metric_name, self.derivative(metric_name, long(stats[s]), self.MAX_VALUES[s]))
