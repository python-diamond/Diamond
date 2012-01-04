
from diamond import *
import diamond.collector
import os

from collections import namedtuple

# http://www.kernel.org/doc/Documentation/iostats.txt

_FileSystem = namedtuple('FileSystem', 'device, mount_point')
_DiskStatistics = namedtuple('DiskStatistics', '''
    device,
    reads, reads_merged, reads_sectors,  reads_milliseconds,
    writes, writes_merged, writes_sectors, writes_milliseconds,
    io_in_progress, io_milliseconds, io_milliseconds_weighted
''')

def get_disk_labels():
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


# iostat(1): Each sector has size of 512 bytes.

def get_file_systems():
    '''
    Creates a map of mounted filesystems on the machine.

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

            result[(major, minor)] = _FileSystem(device, mount_point)

    file.close()
    return result

def get_disk_statistics():
    '''
    Create a map of disks in the machine.

    Returns:
      (major, minor) -> DiskStatistics(device, ...)
    '''
    result = {}
    if not os.access('/proc/diskstats', os.R_OK):
        return result
    file = open('/proc/diskstats')

    for line in file:
        try:
            columns = line.split()
            major, minor, device = int(columns[0]), int(columns[1]), columns[2]

            if device.startswith('ram') or device.startswith('loop'):
                continue

            result[(major, minor)] = _DiskStatistics(device, *map(int, columns[3:]))
        except ValueError:
            continue

    file.close()
    return result
