# coding=utf-8

"""
Collect IO Stats

Note: You may need to artifically generate some IO load on a disk/partition
before graphite will generate the metrics.

 * http://www.kernel.org/doc/Documentation/iostats.txt

#### Dependencies

 * /proc/diskstats

"""

import diamond.collector
import diamond.convertor
import time
import os
import re

try:
    import psutil
    psutil  # workaround for pyflakes issue #13
except ImportError:
    psutil = None


class DiskUsageCollector(diamond.collector.Collector):

    MAX_VALUES = {
        'reads':                    4294967295,
        'reads_merged':             4294967295,
        'reads_milliseconds':       4294967295,
        'writes':                   4294967295,
        'writes_merged':            4294967295,
        'writes_milliseconds':      4294967295,
        'io_milliseconds':          4294967295,
        'io_milliseconds_weighted': 4294967295
    }

    LastCollectTime = None

    def get_default_config_help(self):
        config_help = super(DiskUsageCollector, self).get_default_config_help()
        config_help.update({
            'devices': "A regex of which devices to gather metrics for."
                       + " Defaults to md, sd, xvd, disk, and dm devices",
            'sector_size': 'The size to use to calculate sector usage'
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(DiskUsageCollector, self).get_default_config()
        config.update({
            'enabled':  'True',
            'path':     'iostat',
            'devices':  ('PhysicalDrive[0-9]+$'
                         + '|md[0-9]+$'
                         + '|sd[a-z]+[0-9]*$'
                         + '|x?vd[a-z]+[0-9]*$'
                         + '|disk[0-9]+$'
                         + '|dm\-[0-9]+$'),
            'sector_size': 512
        })
        return config

    def get_disk_statistics(self):
        """
        Create a map of disks in the machine.

        http://www.kernel.org/doc/Documentation/iostats.txt

        Returns:
          (major, minor) -> DiskStatistics(device, ...)
        """
        result = {}

        if os.access('/proc/diskstats', os.R_OK):
            fp = open('/proc/diskstats')

            try:
                for line in fp:
                    try:
                        columns = line.split()
                        # On early linux v2.6 versions, partitions have only 4
                        # output fields not 11. From linux 2.6.25 partitions
                        # have the full stats set.
                        if len(columns) < 14:
                            continue
                        major = int(columns[0])
                        minor = int(columns[1])
                        device = columns[2]

                        if (device.startswith('ram')
                            or device.startswith('loop')):
                            continue

                        result[(major, minor)] = {
                            'device': device,
                            'reads': float(columns[3]),
                            'reads_merged': float(columns[4]),
                            'reads_sectors': float(columns[5]),
                            'reads_milliseconds': float(columns[6]),
                            'writes': float(columns[7]),
                            'writes_merged': float(columns[8]),
                            'writes_sectors': float(columns[9]),
                            'writes_milliseconds': float(columns[10]),
                            'io_in_progress': float(columns[11]),
                            'io_milliseconds': float(columns[12]),
                            'io_milliseconds_weighted': float(columns[13])
                        }
                    except ValueError:
                        continue
            finally:
                fp.close()
        else:
            if not psutil:
                self.log.error('Unable to import psutil')
                return None

            disks = psutil.disk_io_counters(True)
            for disk in disks:
                    result[(0, len(result))] = {
                        'device': disk,
                        'reads': disks[disk].read_count,
                        'reads_merged': 0,
                        'reads_sectors': (disks[disk].read_bytes
                                          / int(self.config['sector_size'])),
                        'reads_milliseconds': disks[disk].read_time,
                        'writes': disks[disk].write_count,
                        'writes_merged': 0,
                        'writes_sectors': (disks[disk].write_bytes
                                           / int(self.config['sector_size'])),
                        'writes_milliseconds': disks[disk].write_time,
                        'io_in_progress': 0,
                        'io_milliseconds':
                        disks[disk].read_time + disks[disk].write_time,
                        'io_milliseconds_weighted':
                        disks[disk].read_time + disks[disk].write_time
                    }

        return result

    def collect(self):

        # Handle collection time intervals correctly
        CollectTime = time.time()
        time_delta = float(self.config['interval'])
        if self.LastCollectTime:
            time_delta = CollectTime - self.LastCollectTime
        if not time_delta:
            time_delta = float(self.config['interval'])
        self.LastCollectTime = CollectTime

        exp = self.config['devices']
        reg = re.compile(exp)

        results = self.get_disk_statistics()
        if not results:
            self.log.error('No diskspace metrics retrieved')
            return None

        for key, info in results.iteritems():
            metrics = {}

            name = info['device']
            if not reg.match(name):
                continue

            for key, value in info.iteritems():
                if key == 'device':
                    continue
                oldkey = key

                for unit in self.config['byte_unit']:
                    key = oldkey

                    if key.endswith('sectors'):
                        key = key.replace('sectors', unit)
                        value /= (1024 / int(self.config['sector_size']))
                        value = diamond.convertor.binary.convert(value=value,
                                                                 oldUnit='kB',
                                                                 newUnit=unit)
                        self.MAX_VALUES[key] = diamond.convertor.binary.convert(
                            value=diamond.collector.MAX_COUNTER,
                            oldUnit='byte',
                            newUnit=unit)

                    metric_name = '.'.join([info['device'], key])
                    # io_in_progress is a point in time counter, !derivative
                    if key != 'io_in_progress':
                        metric_value = self.derivative(
                            metric_name,
                            value,
                            self.MAX_VALUES[key],
                            time_delta=False)
                    else:
                        metric_value = value

                    metrics[key] = metric_value

            metrics['read_requests_merged_per_second'] = (
                metrics['reads_merged'] / time_delta)
            metrics['write_requests_merged_per_second'] = (
                metrics['writes_merged'] / time_delta)
            metrics['reads_per_second'] = metrics['reads'] / time_delta
            metrics['writes_per_second'] = metrics['writes'] / time_delta

            for unit in self.config['byte_unit']:
                metric_name = 'read_%s_per_second' % unit
                key = 'reads_%s' % unit
                metrics[metric_name] = metrics[key] / time_delta

                metric_name = 'write_%s_per_second' % unit
                key = 'writes_%s' % unit
                metrics[metric_name] = metrics[key] / time_delta

                # Set to zero so the nodes are valid even if we have 0 io for
                # the metric duration
                metric_name = 'average_request_size_%s' % unit
                metrics[metric_name] = 0

            metrics['io'] = metrics['reads'] + metrics['writes']

            metrics['average_queue_length'] = (
                metrics['io_milliseconds_weighted']
                / time_delta
                / 1000.0)

            metrics['util_percentage'] = (metrics['io_milliseconds']
                                          / time_delta
                                          / 10.0)

            metrics['iops'] = 0
            metrics['service_time'] = 0
            metrics['await'] = 0
            metrics['read_await'] = 0
            metrics['write_await'] = 0
            metrics['concurrent_io'] = 0

            if metrics['reads'] > 0:
                metrics['read_await'] = (metrics['reads_milliseconds']
                                         / metrics['reads'])
            if metrics['writes'] > 0:
                metrics['write_await'] = (metrics['writes_milliseconds']
                                          / metrics['writes'])

            if metrics['io'] > 0:
                for unit in self.config['byte_unit']:
                    rkey = 'reads_%s' % unit
                    wkey = 'writes_%s' % unit
                    metric_name = 'average_request_size_%s' % unit
                    metrics[metric_name] = (metrics[rkey]
                                            + metrics[wkey]) / metrics['io']

                metrics['iops'] = metrics['io'] / time_delta

                metrics['service_time'] = (metrics['io_milliseconds']
                                           / metrics['io'])

                metrics['await'] = ((metrics['reads_milliseconds']
                                     + metrics['writes_milliseconds'])
                                    / metrics['io'])

                # http://www.scribd.com/doc/15013525
                # Page 28
                metrics['concurrent_io'] = (metrics['reads_per_second']
                                            + metrics['writes_per_second']
                                            ) * (metrics['service_time']
                                                 / 1000.0)

                # Only publish when we have io figures
                for key in metrics:
                    metric_name = '.'.join([info['device'],
                                            key]).replace('/', '_')
                    self.publish(metric_name, metrics[key])
