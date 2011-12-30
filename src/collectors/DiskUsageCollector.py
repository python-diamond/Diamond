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

import disk

class DiskUsageCollector(diamond.collector.Collector):
    """
    Collect IO Stats
    """
    MAX_VALUES = {
        'reads':                    4294967295,
        'reads_merged':             4294967295,
        'reads_milliseconds':       4294967295,
        'writes':                   4294967295,
        'writes_merged':            4294967295,
        'writes_milliseconds':      4294967295,
        'io_in_progress':           diamond.collector.MAX_COUNTER,
        'io_milliseconds':          4294967295,
        'io_milliseconds_weighted': 4294967295
    }

    def collect(self):
        for key, info in disk.get_disk_statistics().iteritems():
            metrics = {}

            name = info.device
            # TODO: Make this configurable
            if not re.match(r'md[0-9]$|sd[a-z]+$|xvd[a-z]+$', name):
                continue

            for key, value in info._asdict().iteritems():
                if key == 'device':
                    continue

                if key.endswith('sectors'):
                    key = key.replace('sectors', self.config['byte_unit'])
                    # Assume 512 byte sectors
                    # TODO: Fix me to be detectable
                    value = value / 2
                    value = diamond.convertor.binary.convert(value = value, oldUnit = 'kB', newUnit = self.config['byte_unit'])
                    self.MAX_VALUES[key] = diamond.convertor.binary.convert(value = diamond.collector.MAX_COUNTER, oldUnit = 'Byte', newUnit = self.config['byte_unit'])

                metric_name = '.'.join([info.device, key])
                metric_value = self.derivative(metric_name, value, self.MAX_VALUES[key])

                metrics[key] = metric_value

            # TODO: Make this correct!
            time_delta = self.config['interval']

            metrics['read_requests_merged_per_second']  = metrics['reads_merged'] / time_delta
            metrics['write_requests_merged_per_second'] = metrics['writes_merged'] / time_delta
            metrics['reads_per_second']                 = metrics['reads'] / time_delta
            metrics['writes_per_second']                = metrics['writes'] / time_delta

            metric_name = 'read_%s_per_second' % (self.config['byte_unit'])
            key = 'reads_%s' % (self.config['byte_unit'])
            metrics[metric_name]                        = metrics[key] / time_delta

            metric_name = 'write_%s_per_second' % (self.config['byte_unit'])
            key = 'writes_%s' % (self.config['byte_unit'])
            metrics[metric_name]                        = metrics[key] / time_delta

            metric_name = 'average_request_size_%s' % (self.config['byte_unit'])
            metrics[metric_name]                        = 0
            metrics['average_queue_length']             = metrics['io_milliseconds'] / time_delta * 1000
            metrics['await']                            = 0
            metrics['service_time']                     = 0
            metrics['util_percentage']                  = (metrics['io_milliseconds'] / (time_delta * 1000)) * 100
            metrics['iops']                             = (metrics['reads'] + metrics['writes']) / time_delta
            metrics['io']                               = metrics['reads'] + metrics['writes']
            metrics['concurrent_io']                    = 0

            if metrics['io'] > 0:
                rkey = 'reads_%s' % (self.config['byte_unit'])
                wkey = 'writes_%s' % (self.config['byte_unit'])
                metric_name = 'average_request_size_%s' % (self.config['byte_unit'])

                metrics[metric_name]                    = (metrics[rkey] + metrics[wkey] ) / metrics['io']
                metrics['service_time']                 = metrics['io_milliseconds'] / metrics['io']
                metrics['await']                        = metrics['io_milliseconds_weighted'] / metrics['io']

                # http://www.scribd.com/doc/15013525/Your-Disk-Array-is-Slower-Than-it-Should-Be Page 28
                metrics['concurrent_io']                = round((metrics['reads_per_second'] + metrics['writes_per_second']) * (metrics['service_time'] / 1000), 1);

                # Only publish when we have io figures
                for key in metrics:
                    metric_name = '.'.join([info.device, key])
                    self.publish(metric_name, metrics[key])
