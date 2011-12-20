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

import disk

class DiskSpaceCollector(diamond.collector.Collector):
    """
    Uses /proc/mounts and os.statvfs() to get disk space usage
    """    
    def collect(self):
        for key, info in disk.get_file_systems().iteritems():
            name = info.mount_point.replace('/', '_')
            name = 'root' if name == '_' else name

            data = os.statvfs(info.mount_point)
            block_size = data.f_bsize

            blocks_total, blocks_free, blocks_avail = data.f_blocks, data.f_bfree, data.f_bavail
            inodes_total, inodes_free, inodes_avail = data.f_files, data.f_ffree, data.f_favail

            metric_name = '%s.gbytes_used' % name
            metric_value = float(block_size) * float(blocks_total - blocks_free)
            metric_value = diamond.convertor.bytes_to_gbytes(metric_value)
            self.publish(metric_name, metric_value, 2)

            metric_name = '%s.gbytes_free' % name
            metric_value = float(block_size) * float(blocks_free)
            metric_value = diamond.convertor.bytes_to_gbytes(metric_value)
            self.publish(metric_name, metric_value, 2)

            metric_name = '%s.gbytes_avail' % name
            metric_value = float(block_size) * float(blocks_avail)
            metric_value = diamond.convertor.bytes_to_gbytes(metric_value)
            self.publish(metric_name, metric_value, 2)

            self.publish('%s.inodes_used'  % name, inodes_total - inodes_free)
            self.publish('%s.inodes_free'  % name, inodes_free)
            self.publish('%s.inodes_avail' % name, inodes_avail)
