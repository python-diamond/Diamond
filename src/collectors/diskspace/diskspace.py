# coding=utf-8

"""
Uses /proc/mounts and os.statvfs() to get disk space usage

#### Dependencies

 * /proc/mounts

#### Examples

    # no exclude filters at all
    exclude_filters =,

    # exclude everything that begins /boot or /mnt
    exclude_filters = ^/boot, ^/mnt

    # exclude everything that includes the letter 'm'
    exclude_filters = m,

"""

import diamond.collector
import diamond.convertor
import os
import re

try:
    import psutil
except ImportError:
    psutil = None


class DiskSpaceCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(DiskSpaceCollector, self).get_default_config_help()
        config_help.update({
            'filesystems': "filesystems to examine",
            'exclude_filters':
                "A list of regex patterns. Any filesystem" +
                " matching any of these patterns will be excluded from disk" +
                " space metrics collection",
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(DiskSpaceCollector, self).get_default_config()
        config.update({
            'path': 'diskspace',
            # filesystems to examine
            'filesystems': 'ext2, ext3, ext4, xfs, glusterfs, nfs, nfs4, ' +
                           ' ntfs, hfs, fat32, fat16, btrfs',

            # exclude_filters
            #   A list of regex patterns
            #   A filesystem matching any of these patterns will be excluded
            #   from disk space metrics collection.
            #
            # Examples:
            #       exclude_filters =,
            # no exclude filters at all
            #       exclude_filters = ^/boot, ^/mnt
            # exclude everything that begins /boot or /mnt
            #       exclude_filters = m,
            # exclude everything that includes the letter "m"
            'exclude_filters': ['^/export/home'],

            # Default numeric output
            'byte_unit': ['byte']
        })
        return config

    def process_config(self):
        super(DiskSpaceCollector, self).process_config()
        # Precompile things
        self.exclude_filters = self.config['exclude_filters']
        if isinstance(self.exclude_filters, str):
            self.exclude_filters = [self.exclude_filters]

        if not self.exclude_filters:
            self.exclude_reg = re.compile('!.*')
        else:
            self.exclude_reg = re.compile('|'.join(self.exclude_filters))

        self.filesystems = []
        if isinstance(self.config['filesystems'], str):
            for filesystem in self.config['filesystems'].split(','):
                self.filesystems.append(filesystem.strip())
        elif isinstance(self.config['filesystems'], list):
            self.filesystems = self.config['filesystems']

    def get_disk_labels(self):
        """
        Creates a mapping of device nodes to filesystem labels
        """
        path = '/dev/disk/by-label/'
        labels = {}
        if not os.path.isdir(path):
            return labels

        for label in os.listdir(path):
            label = label.replace('\\x2f', '/')
            device = os.path.realpath(path + '/' + label)
            labels[device] = label

        return labels

    def get_file_systems(self):
        """
        Creates a map of mounted filesystems on the machine.

        iostat(1): Each sector has size of 512 bytes.

        Returns:
          st_dev -> FileSystem(device, mount_point)
        """
        result = {}
        if os.access('/proc/mounts', os.R_OK):
            file = open('/proc/mounts')
            for line in file:
                try:
                    mount = line.split()
                    device = mount[0]
                    mount_point = mount[1]
                    fs_type = mount[2]
                except (IndexError, ValueError):
                    continue

                # Skip the filesystem if it is not in the list of valid
                # filesystems
                if fs_type not in self.filesystems:
                    self.log.debug("Ignoring %s since it is of type %s " +
                                   " which is not in the list of filesystems.",
                                   mount_point, fs_type)
                    continue

                # Process the filters
                if self.exclude_reg.search(mount_point):
                    self.log.debug("Ignoring %s since it is in the " +
                                   "exclude_filter list.", mount_point)
                    continue

                if ((('/' in device or device == 'tmpfs') and
                     mount_point.startswith('/'))):
                    try:
                        stat = os.stat(mount_point)
                    except OSError:
                        self.log.debug("Path %s is not mounted - skipping.",
                                       mount_point)
                        continue

                    if stat.st_dev in result:
                        continue

                    result[stat.st_dev] = {
                        'device': os.path.realpath(device),
                        'mount_point': mount_point,
                        'fs_type': fs_type
                    }

            file.close()

        else:
            if not psutil:
                self.log.error('Unable to import psutil')
                return None

            partitions = psutil.disk_partitions(False)
            for partition in partitions:
                result[len(result)] = {
                    'device': os.path.realpath(partition.device),
                    'mount_point': partition.mountpoint,
                    'fs_type': partition.fstype
                }
            pass

        return result

    def collect(self):
        labels = self.get_disk_labels()
        results = self.get_file_systems()
        if not results:
            self.log.error('No diskspace metrics retrieved')
            return None

        for key, info in results.items():
            if info['device'] in labels:
                name = labels[info['device']]
            else:
                name = info['mount_point'].replace('/', '_')
                name = name.replace('.', '_').replace('\\', '')
                if name == '_':
                    name = 'root'
                if name == '_tmp':
                    name = 'tmp'

            if hasattr(os, 'statvfs'):  # POSIX
                try:
                    data = os.statvfs(info['mount_point'])
                except OSError as e:
                    self.log.exception(e)
                    continue

                # Changed from data.f_bsize as f_frsize seems to be a more
                # accurate representation of block size on multiple POSIX
                # operating systems.
                block_size = data.f_frsize

                blocks_total = data.f_blocks
                blocks_free = data.f_bfree
                blocks_avail = data.f_bavail
                inodes_total = data.f_files
                inodes_free = data.f_ffree
                inodes_avail = data.f_favail

            elif os.name == 'nt':       # Windows
                # fixme: used still not exact compared to disk_usage.py
                # from psutil
                raw_data = psutil.disk_usage(info['mount_point'])

                block_size = 1  # fixme: ?

                blocks_total = raw_data.total
                blocks_free = raw_data.free

            else:
                raise NotImplementedError("platform not supported")

            for unit in self.config['byte_unit']:
                metric_name = '%s.%s_percentfree' % (name, unit)
                metric_value = float(blocks_free) / float(
                    blocks_free + (blocks_total - blocks_free)) * 100
                self.publish_gauge(metric_name, metric_value, 2)

                metric_name = '%s.%s_used' % (name, unit)
                metric_value = float(block_size) * float(
                    blocks_total - blocks_free)
                metric_value = diamond.convertor.binary.convert(
                    value=metric_value, oldUnit='byte', newUnit=unit)
                self.publish_gauge(metric_name, metric_value, 2)

                metric_name = '%s.%s_free' % (name, unit)
                metric_value = float(block_size) * float(blocks_free)
                metric_value = diamond.convertor.binary.convert(
                    value=metric_value, oldUnit='byte', newUnit=unit)
                self.publish_gauge(metric_name, metric_value, 2)

                if os.name != 'nt':
                    metric_name = '%s.%s_avail' % (name, unit)
                    metric_value = float(block_size) * float(blocks_avail)
                    metric_value = diamond.convertor.binary.convert(
                        value=metric_value, oldUnit='byte', newUnit=unit)
                    self.publish_gauge(metric_name, metric_value, 2)

            if os.name != 'nt':
                if float(inodes_total) > 0:
                    self.publish_gauge(
                        '%s.inodes_percentfree' % name,
                        float(inodes_free) / float(inodes_total) * 100)
                self.publish_gauge('%s.inodes_used' % name,
                                   inodes_total - inodes_free)
                self.publish_gauge('%s.inodes_free' % name, inodes_free)
                self.publish_gauge('%s.inodes_avail' % name, inodes_avail)
