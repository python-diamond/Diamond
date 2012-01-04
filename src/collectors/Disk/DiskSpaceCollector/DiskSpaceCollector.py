
from diamond import *
import diamond.collector
import diamond.convertor

import disk

class DiskSpaceCollector(diamond.collector.Collector):
    """
    Uses /proc/mounts and os.statvfs() to get disk space usage
    """
    def collect(self):
        labels = disk.get_disk_labels()
        for key, info in disk.get_file_systems().iteritems():
            if labels.has_key(info.device):
                name = labels[info.device]
            else:
                name = info.mount_point.replace('/', '_')
                name = 'root' if name == '_' else name

            data = os.statvfs(info.mount_point)
            block_size = data.f_bsize

            blocks_total, blocks_free, blocks_avail = data.f_blocks, data.f_bfree, data.f_bavail
            inodes_total, inodes_free, inodes_avail = data.f_files, data.f_ffree, data.f_favail

            metric_name = '%s.%s_used' % (name, self.config['byte_unit'])
            metric_value = float(block_size) * float(blocks_total - blocks_free)
            metric_value = diamond.convertor.binary.convert(value = metric_value, oldUnit = 'Byte', newUnit = self.config['byte_unit'])
            self.publish(metric_name, metric_value, 2)

            metric_name = '%s.%s_free' % (name, self.config['byte_unit'])
            metric_value = float(block_size) * float(blocks_free)
            metric_value = diamond.convertor.binary.convert(value = metric_value, oldUnit = 'Byte', newUnit = self.config['byte_unit'])
            self.publish(metric_name, metric_value, 2)

            metric_name = '%s.%s_avail' % (name, self.config['byte_unit'])
            metric_value = float(block_size) * float(blocks_avail)
            metric_value = diamond.convertor.binary.convert(value = metric_value, oldUnit = 'Byte', newUnit = self.config['byte_unit'])
            self.publish(metric_name, metric_value, 2)

            self.publish('%s.inodes_used'  % name, inodes_total - inodes_free)
            self.publish('%s.inodes_free'  % name, inodes_free)
            self.publish('%s.inodes_avail' % name, inodes_avail)
