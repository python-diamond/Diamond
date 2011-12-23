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
import os

from collections import namedtuple

# http://www.kernel.org/doc/Documentation/iostats.txt

_FileSystem = namedtuple('FileSystem', 'device, mount_point')
_DiskStatistics = namedtuple('DiskStatistics', '''
    device,
    reads, reads_merged, reads_sectors,  reads_milliseconds,
    writes, writes_merged, writes_sectors, writes_milliseconds,
    iops_in_progress, io_milliseconds, io_milliseconds_weighted
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
