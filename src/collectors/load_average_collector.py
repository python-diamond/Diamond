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

class LoadAverageCollector(diamond.collector.Collector):
    """
    Uses /proc/loadavg to collect data on load average
    """

    PROC = '/proc/loadavg'

    def collect(self):
        """
        Collect load average stats
        """
        results = {}
        # open file
        file = open(self.PROC, 'r')
        # Build regex
        exp = '^([0-9\.]+)\s*([0-9\.]+)\s*([0-9\.]+)\s*([0-9]+)\/([0-9]+)'
        reg = re.compile(exp)
        for line in file:
            match = reg.match(line)
            if match:
                results['01'] = match.group(1)
                results['05'] = match.group(2)
                results['15'] = match.group(3)
                results['processes.running'] = match.group(4)
                results['processes.total'] = match.group(5)
        # Close file
        file.close()

        for k in results.keys():
            self.publish(k, results[k], 2)
