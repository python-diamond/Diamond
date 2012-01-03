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
import diamond.convertor

class NetworkCollector(diamond.collector.Collector):
    """
    The NetworkCollector class collects metrics on network interface usage
    using /proc/net/dev.
    """

    PROC = '/proc/net/dev'

    MAX_VALUES = {
        'rx_bytes':      diamond.collector.MAX_COUNTER,
        'rx_packets':    diamond.collector.MAX_COUNTER,
        'rx_errors':     diamond.collector.MAX_COUNTER,
        'rx_drop':       diamond.collector.MAX_COUNTER,
        'rx_fifo':       diamond.collector.MAX_COUNTER,
        'rx_frame':      diamond.collector.MAX_COUNTER,
        'rx_compressed': diamond.collector.MAX_COUNTER,
        'rx_multicast':  diamond.collector.MAX_COUNTER,
        'tx_bytes':      diamond.collector.MAX_COUNTER,
        'tx_packets':    diamond.collector.MAX_COUNTER,
        'tx_errors':     diamond.collector.MAX_COUNTER,
        'tx_drop':       diamond.collector.MAX_COUNTER,
        'tx_fifo':       diamond.collector.MAX_COUNTER,
        'tx_frame':      diamond.collector.MAX_COUNTER,
        'tx_compressed': diamond.collector.MAX_COUNTER,
        'tx_multicast':  diamond.collector.MAX_COUNTER,
        }

    def collect(self):
        """
        Collect network interface stats.
        """

        if not os.access(self.PROC, os.R_OK):
            return None

        # Initialize results
        results = {}
        # Open File
        file = open(self.PROC)
        # Build Regular Expression
        exp = '^(?:\s*)([%s0-9]+):(?:\s*)(?P<rx_bytes>\d+)(?:\s*)(?P<rx_packets>\w+)(?:\s*)(?P<rx_errors>\d+)(?:\s*)(?P<rx_drop>\d+)(?:\s*)(?P<rx_fifo>\d+)(?:\s*)(?P<rx_frame>\d+)(?:\s*)(?P<rx_compressed>\d+)(?:\s*)(?P<rx_multicast>\d+)(?:\s*)(?P<tx_bytes>\d+)(?:\s*)(?P<tx_packets>\w+)(?:\s*)(?P<tx_errors>\d+)(?:\s*)(?P<tx_drop>\d+)(?:\s*)(?P<tx_fifo>\d+)(?:\s*)(?P<tx_frame>\d+)(?:\s*)(?P<tx_compressed>\d+)(?:\s*)(?P<tx_multicast>\d+)(?:.*)$' % ( '|'.join(self.config['interfaces']) )
        reg = re.compile(exp)
        # Match Interfaces
        for line in file:
            match = reg.match(line)
            if match:
                device = match.group(1)
                results[device] = match.groupdict()
        # Close File
        file.close()

        for device in results:
            stats = results[device]
            for s,v in stats.items():
                # Get Metric Name
                metric_name = '.'.join([device, s])
                # Get Metric Value
                metric_value = self.derivative(metric_name, long(v), self.MAX_VALUES[s])

                # Convert rx_bytes and tx_bytes
                if s == 'rx_bytes' or s == 'tx_bytes':
                    convertor = diamond.convertor.binary(value = metric_value, unit = 'Byte')

                    for u in self.config['byte_unit'].split():
                        # Public Converted Metric
                        self.publish(metric_name.replace('bytes', u), convertor.get(unit = u))
                else:
                    # Publish Metric Derivative
                    self.publish(metric_name, metric_value)
