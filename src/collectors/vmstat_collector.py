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

class VMStatCollector(diamond.collector.Collector):
    """
    Uses /proc/vmstat to collect data on virtual memory manager 
    """

    PROC = '/proc/vmstat'
    MAX_VALUES = {
        'pgpgin': diamond.collector.MAX_COUNTER,
        'pgpgout': diamond.collector.MAX_COUNTER,
        'pswpin': diamond.collector.MAX_COUNTER,
        'pswpout': diamond.collector.MAX_COUNTER,
    }

    def collect(self):
        """
        Collect vm stats
        """
        results = {}
        # open file
        file = open(self.PROC)
        exp = '^(pgpgin|pgpgout|pswpin|pswpout)\s(\d+)'
        reg = re.compile(exp) 
        # Build regex
        for line in file:
            match = reg.match(line)
            if match:
                metric_name = match.group(1)
                metric_value = match.group(2)
                results[metric_name] = self.derivative(metric_name, int(metric_value), self.MAX_VALUES[metric_name])
            
        # Close file
        file.close()

        for k in results.keys():
            self.publish(k, results[k], 2)
