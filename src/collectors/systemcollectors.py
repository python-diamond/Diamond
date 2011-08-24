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

import os
import sys
import re 
import logging
import time
import datetime
import random
import urllib2
import base64
import csv
from urlparse import urlparse

import diamond.collector

class TCPStatsCollector(diamond.collector.Collector):
    """
    The TCPStatsCollector class collects metrics on TCP stats from 
    /proc/net/netstat
    """

    PROC='/proc/net/netstat'

    def collect(self):
        """
        Collect TCP data
        """
        #Build regex
        exp = '^TcpExt: ((\w*|\d*).+)'
        reg = re.compile(exp,re.M)
        #Initialize Variables
        rawData=[]
        results={}
        #Open PROC file
        file=open(self.PROC,'r')
        #Get data
        for line in file:
            match = reg.match(line)
            if match:
                rawData.append(match.group(1))
        #Close file
        file.close()
        #Parse data
        stats=rawData.pop().split()
        metric=rawData.pop().split()
        #Reverse stats for building the dictionary correctly
        stats.reverse()
        #Build dictionary
        for y in metric:
            results[y]=stats.pop()
        for k in results.keys():
            self.publish(k, results[k], 0)
    

class NetworkCollector(diamond.collector.Collector):
    """
    The NetworkCollector class collects metrics on network interface usage
    using /proc/net/dev.
    """

    PROC = '/proc/net/dev'

    MAX_VALUES = {
        'rx_bytes': 18446744073709600000, 
        'rx_packets': 18446744073709600000, 
        'rx_errors': 18446744073709600000,
        'rx_drop': 18446744073709600000,
        'rx_fifo': 18446744073709600000,
        'rx_frame': 18446744073709600000,
        'rx_compressed': 18446744073709600000,
        'rx_multicast': 18446744073709600000,
        'tx_bytes': 18446744073709600000,
        'tx_packets': 18446744073709600000,
        'tx_errors': 18446744073709600000,
        'tx_drop': 18446744073709600000,
        'tx_fifo': 18446744073709600000,
        'tx_frame': 18446744073709600000,
        'tx_compressed': 18446744073709600000,
        'tx_multicast': 18446744073709600000,
        }
        
    def convert_to_mbit(self, value):
        """
        Convert bytes to megabits.
        """
        return ((float(value) / 1024.0 / 1024.0) * 8.0 )

    def convert_to_kbit(self, value):
        """
        Convert bytes to kilobits.
        """
        return ((float(value) / 1024.0 ) * 8.0 )

    def convert_to_mbyte(self, value):
        """
        Convert bytes to megabytes.
        """
        return (float(value) / 1024.0 / 1024.0)

    def convert_to_kbyte(self, value):
        """
        Convert bytes to kilobytes.
        """
        return (float(value) / 1024.0 ) 

    def collect(self):
        """
        Collect network interface stats.
        """
        # Initialize Units
        units = {
            'mbit': self.convert_to_mbit, 
            'kbit': self.convert_to_kbit,
            'mbyte': self.convert_to_mbyte,
            'kbyte': self.convert_to_kbyte,
            }
        # Initialize results
        results = {}
        # Open File
        file = open(self.PROC, 'r')
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
                # Publish Metric Derivative
                self.publish(metric_name, metric_value) 
                # Convert rx_bytes and tx_bytes
                if s == 'rx_bytes' or s == 'tx_bytes':
                    for u in units: 
                        # Public Converted Metric  
                        self.publish(metric_name.replace('bytes', u), units[u](metric_value))

class MemoryCollector(diamond.collector.Collector):
    """
    This class collects data on memory utilization

    /proc/meminfo is used to gather the data, which is returned in units of kB
    """
    
    PROC = '/proc/meminfo'

    def collect(self):
        """
        Collect memory stats
        """
        results = {}
        # Open file
        file = open(self.PROC)
        # Build regular expression
        exp = '^(MemTotal|MemFree|Buffers|Cached|SwapCached|Active|Inactive|SwapTotal|SwapFree|Dirty|VmallocTotal|VmallocUser|VmallocChunk):\s*(\d+)\s*kB'
        reg = re.compile(exp)
        for line in file:
            match = reg.match(line)
            if match:
                results[match.group(1)] = match.group(2)
        # Close file
        file.close()

        for k in results.keys():
            self.publish(k, results[k], 0)

class LoadAverageCollector(diamond.collector.Collector):
    """
    Uses /proc/loadavg to collect data on load average
    """
    
    # Collector Path: Path where collector will store its metrics 
    COLLECTOR_PATH = 'loadavg'

    PROC = '/proc/loadavg'

    def collect(self):
        """
        Collect load average stats
        """
        results = {}
        # open file
        file = open(self.PROC)
        # Build regex
        exp = '^([0-9\.]+)\s*([0-9\.]+)\s*([0-9\.]+)\s*([0-9]+)\/([0-9]+)'
        reg = re.compile(exp)
        for line in file:
            match = reg.match(line)
            if match:
                results['1minute'] = match.group(1)
                results['5minute'] = match.group(2)
                results['10minute'] = match.group(3)
                results['processes.running'] = match.group(4)
                results['processes.total'] = match.group(5)
        # Close file
        file.close()

        for k in results.keys():
            self.publish(k, results[k], 2)

class CPUCollector(diamond.collector.Collector):
    """
    The CPUCollector collects CPU utilization metric using /proc/stat.
    """

    PROC = '/proc/stat'
    MAX_VALUES = {
        'user': 18446744073709551615,
        'nice': 18446744073709551615,
        'system': 18446744073709551615,
        'idle': 18446744073709551615,
        'iowait': 18446744073709551615,
    }

    def collect(self):
        """
        Collector cpu stats
        """
        results = {}
        # Open file
        file = open(self.PROC, 'r')
        # Build Regex
        exp = '^(cpu[0-9]*)\s+(?P<user>\d+)\s+(?P<nice>\d+)\s+(?P<system>\d+)\s+(?P<idle>\d+)\s+(?P<iowait>\d+).*$'
        reg = re.compile(exp)
        for line in file:
            match = reg.match(line)
            if match:
                cpu = match.group(1)
                if cpu == 'cpu':
                    cpu = 'total'
                results[cpu] = {}
                results[cpu] = match.groupdict()
        # Close File
        file.close()
        
        for cpu in results.keys():
            stats = results[cpu]
            for s in stats.keys():
                # Get Metric Name 
                metric_name = '.'.join([cpu, s])
                # Publish Metric Derivative
                self.publish(metric_name, self.derivative(metric_name, long(stats[s]), self.MAX_VALUES[s]))


class IOCollector(diamond.collector.Collector):
    """
    Collect IO Stats
    """
    MAX_VALUES = {
        'reads': 4294967295,
        'reads_merged': 4294967295,
        'reads_sectors': 18446744073709551615,
        'reads_kilobytes': 9223372036854775808,
        'reads_milliseconds': 4294967295,
        'writes': 4294967295,
        'writes_merged': 4294967295,
        'writes_sectors': 18446744073709551615,
        'writes_kilobytes': 9223372036854775808,
        'writes_milliseconds': 4294967295,
        'io_milliseconds': 4294967295,
        'weighted_io_milliseconds': 4294967295
    }

    def create_filesystem_list(self):
        """
        Create a list of the mounted filesystems on the machine

        Returns a list of tuples in the form (device, mountpoint, major, minor)
        """
        fs = []
        fd = open('/proc/mounts', 'r')
        for line in fd:
            l = line.split()
            if l[0][0:1] == "/" and l[1][0:1] == "/" and l[1][1:4] not in ['dev', 'proc', 'sys'] and l[0][5:9] not in ['loop']:
                s = os.stat(l[1])
                major = str(os.major(s.st_dev))
                minor = str(os.minor(s.st_dev))
                fs.append((l[0], l[1], major, minor))
        return fs
                
    def create_diskstats_list(self):
        """
        Create a list of the disks for which we have stats
        """
        stats = []
        fd = open('/proc/diskstats', 'r')
        for line in fd:
            l = line.split()
            if l[2][0:3] != 'ram':
                stats.append(l)
        fd.close()
        return stats

    def collect(self):
        """
        Collect IO stats
        """
        # Get a list of the filesystems on the machine
        filesystems = self.create_filesystem_list()
        # Get the devices for which we have stats, and the current stats
        diskstats = self.create_diskstats_list()
        # Iterate through the filesystems, and try to match with an appropriate device
        for fs in filesystems:
            for dev in diskstats:
                if fs[2] == dev[0] and fs[3] == dev[1]:
                    if re.match("xvd", dev[2]):
                        # Python doesn't have sscanf.  Boo!
                        dev_stats = {
                            'reads': dev[3], 
                            'reads_sectors': dev[4], 
                            'reads_kilobytes': int(int(dev[4]) / 2), 
                            'writes': dev[5], 
                            'writes_sectors': dev[6],
                            'writes_kilobytes': int(int(dev[6]) / 2),
                        }
                    else:
                        # Python doesn't have sscanf.  Boo!
                        dev_stats = {
                            'reads': dev[3], 
                            'reads_merged': dev[4], 
                            'reads_sectors': dev[5], 
                            'reads_kilobytes': int(int(dev[5]) / 2), 
                            'reads_milliseconds': dev[6], 
                            'writes': dev[7], 
                            'writes_merged': dev[8], 
                            'writes_sectors': dev[9],
                            'writes_kilobytes': int(int(dev[9]) / 2),
                            'writes_milliseconds': dev[10],
                            'io_milliseconds': dev[12],
                            'weighted_io_milliseconds': dev[13]
                        }
                    # replace internal slashes in the filesystem name
                    fs_name = fs[1].replace('/', '_')
                    for m in dev_stats.keys():
                        # Create the metric name
                        metric_name = '.'.join([fs_name, m])
                        # Publish the stat
                        self.publish(metric_name, self.derivative(metric_name, long(dev_stats[m]), self.MAX_VALUES[m]))
                    break

class VMStatCollector(diamond.collector.Collector):
    """
    Uses /proc/vmstat to collect data on virtual memory manager 
    """

    PROC = '/proc/vmstat'
    MAX_VALUES = {
        'pgpgin': 18446744073709551615,
        'pgpgout': 18446744073709551615,
        'pswpin': 18446744073709551615,
        'pswpout': 18446744073709551615,
    }

    def collect(self):
        """
        Collect vm stats
        """
        results = {}
        # open file
        file = open(self.PROC)
        exp = '^(pgpgin|pgpgout|pswpin|pswpout)\s(\d+)'
        reg = re.compile(exp) 
        # Build regex
        for line in file:
            match = reg.match(line)
            if match:
                metric_name = match.group(1)
                metric_value = match.group(2)
                results[metric_name] = self.derivative(metric_name, long(metric_value), self.MAX_VALUES[metric_name])
            
        # Close file
        file.close()

        for k in results.keys():
            self.publish(k, results[k], 2)

class DiskSpaceCollector(diamond.collector.Collector):
    """
    Uses /prc/mounts and os.statvfs() to get disk space usage
    """    
    # Call os.statvfs to get filesystme stats
    STATVFS= [ 'block_size', 'block_size', 'blocks_used', 'blocks_free', 'blocks_avail', 'inodes_used', 'inodes_free', 'inodes_avail' ]

    def is_filtered(self, mountpoint):
        """
        Checks whether a given filesystem should be filtered from having metrics 
        gathered.

        Returns True if the filesystem should be ignored.

        Returns False if the filesystem should be considered.
        """
        if 'exclude_filters' in self.config and len(self.config['exclude_filters']) > 0:
            
            # Catch the most likely error, giving a string value in the config instead of a list
            if isinstance(self.config['exclude_filters'], str):
                self.config['exclude_filters'] = [ self.config['exclude_filters'] ]

            # Loop through the list of filters, and for each check if the given mountpoint matches. Return True if so.
            for f in self.config['exclude_filters']:
                if re.search(f, mountpoint):
                    return True

        # Return False if no filters matched, or no filters are defined
        return False

    def get_filesystem_list(self):
        """
        Create a list of the mounted filesystems on the machine

        Returns a list of tuples in the form (device, mountpoint, major, minor)
        """
        fs = []
        fd = open('/proc/mounts', 'r')
        for line in fd:
            l = line.split()
            if l[2] in self.config['filesystems'] and not self.is_filtered(l[1]): 
                s = os.stat(l[1])
                major = str(os.major(s.st_dev))
                minor = str(os.minor(s.st_dev))
                fs.append((l[0], l[1], major, minor))
        fd.close()
        return fs
    
    def convert_to_gbyte(self, value):
        """
        Convert bytes to megabytes.
        """
        return (float(value) / 1024.0 / 1024.0 / 1024.0)
    
    def convert_to_mbyte(self, value):
        """
        Convert bytes to megabytes.
        """
        return (float(value) / 1024.0 / 1024.0)

    def collect(self):
        # Get a list of filesystems
        fslist = self.get_filesystem_list()
        for fs in fslist:
            fsname = fs[1].replace('/','_')
            # Call os.statvfs to get filesystem stats
            data = os.statvfs(fs[1]) 
            # Gather stats and publis 
            for i in range(1, len(self.STATVFS)):
                # Create the metric name
                metric_name = '.'.join([fsname, self.STATVFS[i]])
                metric_value = data[i]
                self.publish(metric_name, metric_value)

            # Report mbyte, and gbyte used, free, and avail
            conv = {'gbyte': self.convert_to_gbyte, 'mbyte': self.convert_to_mbyte}
            for n,f in conv.items():
                # Publish Used
                metric_name = '.'.join([fsname, "%s_used" % (n)])
                metric_value = f(float(data[0]) * float(data[2] - data[3])) 
                self.publish(metric_name, metric_value, 2)
                # Publish Free 
                metric_name = '.'.join([fsname, "%s_free" % (n)])
                metric_value = f(float(data[0]) * float(data[3])) 
                self.publish(metric_name, metric_value, 2)
                # Publish Avail 
                metric_name = '.'.join([fsname, "%s_avail" % (n)])
                metric_value = f(float(data[0]) * float(data[4])) 
                self.publish(metric_name, metric_value, 2)
