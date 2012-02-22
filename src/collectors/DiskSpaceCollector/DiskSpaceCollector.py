
from diamond import *
import diamond.collector
import diamond.convertor
import os

class DiskSpaceCollector(diamond.collector.Collector):
    """
    Uses /proc/mounts and os.statvfs() to get disk space usage
    """
    
    def get_default_config(self):
        """
        Returns the default collector settings
        """
        return {
            # Enabled by default
            'enabled' : True,
            'path' : 'diskspace',
            # filesystems to examine
            'filesystems' : 'ext2, ext3, ext4, xfs, glusterfs, nfs',

            # exclude_filters
            #   A list of regex patterns
            #   A filesystem matching any of these patterns will be excluded from disk space
            #   metrics collection.
            #
            # Examples:
            #       exclude_filters = ,                 # no exclude filters at all
            #       exclude_filters = ^/boot, ^/mnt     # exclude everything that begins /boot or /mnt
            #       exclude_filters = m,                # exclude everything that includes the letter "m"
            'exclude_filters' : '^/export/home',
            
            # We don't use any derivative data to calculate this value
            # Thus we can use a threaded model
            'method' : 'Threaded',
            
            # Default numeric output
            'byte_unit' : 'gigabyte'
        }

    def get_disk_labels(self):
        '''
        Creates a mapping of device nodes to filesystem labels
        '''
        path = '/dev/disk/by-label/'
        labels = {}
        if not os.path.isdir(path):
            return labels
    
        for label in os.listdir(path):
            device = os.path.realpath(path+'/'+label)
            labels[device] = label
    
        return labels
    
    def get_file_systems(self):
        '''
        Creates a map of mounted filesystems on the machine.
        
        iostat(1): Each sector has size of 512 bytes.
    
        Returns:
          (major, minor) -> FileSystem(device, mount_point)
        '''
        result = {}
        if not os.access('/proc/mounts', os.R_OK):
            return result
        file = open('/proc/mounts')
        for line in file:
            try:
                device, mount_point, fs_type, fs_options, dummy1, dummy2 = line.split()
            except ValueError:
                continue
    
            if mount_point.startswith('/dev') or mount_point.startswith('/proc') or mount_point.startswith('/sys'):
                continue
    
            if device.startswith('/') and mount_point.startswith('/'):
                stat  = os.stat(mount_point)
                major = os.major(stat.st_dev)
                minor = os.minor(stat.st_dev)
    
                result[(major, minor)] = {
                    'device'      : device,
                    'mount_point' : mount_point
                }
    
        file.close()
        return result
    
    def collect(self):
        labels = self.get_disk_labels()
        for key, info in self.get_file_systems().iteritems():
            if labels.has_key(info['device']):
                name = labels[info['device']]
            else:
                name = info['mount_point'].replace('/', '_')
                if name == '_':
                    name = 'root'

            data = os.statvfs(info['mount_point'])
            block_size = data.f_bsize

            blocks_total, blocks_free, blocks_avail = data.f_blocks, data.f_bfree, data.f_bavail
            inodes_total, inodes_free, inodes_avail = data.f_files, data.f_ffree, data.f_favail

            metric_name = '%s.%s_used' % (name, self.config['byte_unit'])
            metric_value = float(block_size) * float(blocks_total - blocks_free)
            metric_value = diamond.convertor.binary.convert(value = metric_value, oldUnit = 'byte', newUnit = self.config['byte_unit'])
            self.publish(metric_name, metric_value, 2)

            metric_name = '%s.%s_free' % (name, self.config['byte_unit'])
            metric_value = float(block_size) * float(blocks_free)
            metric_value = diamond.convertor.binary.convert(value = metric_value, oldUnit = 'byte', newUnit = self.config['byte_unit'])
            self.publish(metric_name, metric_value, 2)

            metric_name = '%s.%s_avail' % (name, self.config['byte_unit'])
            metric_value = float(block_size) * float(blocks_avail)
            metric_value = diamond.convertor.binary.convert(value = metric_value, oldUnit = 'byte', newUnit = self.config['byte_unit'])
            self.publish(metric_name, metric_value, 2)

            self.publish('%s.inodes_used'  % name, inodes_total - inodes_free)
            self.publish('%s.inodes_free'  % name, inodes_free)
            self.publish('%s.inodes_avail' % name, inodes_avail)
