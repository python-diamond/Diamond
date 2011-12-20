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
        'reads': 4294967295,
        'reads_merged': 4294967295,
        'reads_kbytes': (((diamond.collector.MAX_COUNTER + 1) / 2) - 1),
        'reads_milliseconds': 4294967295,
        'writes': 4294967295,
        'writes_merged': 4294967295,
        'writes_kbytes': (((diamond.collector.MAX_COUNTER + 1) / 2) - 1),
        'writes_milliseconds': 4294967295,
        'io_milliseconds': 4294967295,
        'io_milliseconds_weighted': 4294967295
    }

    def collect(self):
        for key, info in disk.get_disk_statistics().iteritems():
            name = info.device

            if not re.match(r'md[0-9]$|sd[a-z]+$', name):
                continue

            for key, value in info._asdict().iteritems():
                if key == 'device' or key == 'iops_in_progress':
                    continue

                if key.endswith('sectors'):
                    key = key.replace('sectors', 'kbytes')
                    value = value / 2

                metric_name = '.'.join([info.device, key])
                metric_value = self.derivative(metric_name, value, self.MAX_VALUES[key])

                self.publish(metric_name, metric_value)

