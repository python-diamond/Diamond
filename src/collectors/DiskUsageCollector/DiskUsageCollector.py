
# http://www.kernel.org/doc/Documentation/iostats.txt

from diamond import *
import diamond.collector
import time
import os

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
        'io_milliseconds':          4294967295,
        'io_milliseconds_weighted': 4294967295
    }
    
    LastCollectTime = None

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        return {
            'enabled':  'True',
            'path':     'iostat',
            'devices':  'md[0-9]$|sd[a-z]+$|xvd[a-z]+$'
        }

    def get_disk_statistics(self):
        '''
        Create a map of disks in the machine.
        
        http://www.kernel.org/doc/Documentation/iostats.txt
    
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
    
                result[(major, minor)] = {
                    'device'                   : device,
                    'reads'                    : float(columns[3] ),
                    'reads_merged'             : float(columns[4] ),
                    'reads_sectors'            : float(columns[5] ),
                    'reads_milliseconds'       : float(columns[6] ),
                    'writes'                   : float(columns[7] ),
                    'writes_merged'            : float(columns[8] ),
                    'writes_sectors'           : float(columns[9] ),
                    'writes_milliseconds'      : float(columns[10]),
                    'io_in_progress'           : float(columns[11]),
                    'io_milliseconds'          : float(columns[12]),
                    'io_milliseconds_weighted' : float(columns[13])
                }
            except ValueError:
                continue
    
        file.close()
        return result

    def collect(self):
        
        # Handle collection time intervals correctly
        CollectTime = time.time()
        time_delta = float(self.config['interval'])
        if self.LastCollectTime:
            time_delta = CollectTime-self.LastCollectTime
        if time_delta == 0:
            time_delta = float(self.config['interval'])
        self.LastCollectTime = CollectTime
        
        exp = self.config['devices']
        reg = re.compile(exp)

        for key, info in self.get_disk_statistics().iteritems():
            metrics = {}

            name = info['device']
            if not reg.match(name):
                continue

            for key, value in info.iteritems():
                if key == 'device':
                    continue

                if key.endswith('sectors'):
                    key = key.replace('sectors', self.config['byte_unit'])
                    # Assume 512 byte sectors
                    # TODO: Fix me to be detectable
                    value = value / 2
                    value = diamond.convertor.binary.convert(value = value, oldUnit = 'kB', newUnit = self.config['byte_unit'])
                    self.MAX_VALUES[key] = diamond.convertor.binary.convert(value = diamond.collector.MAX_COUNTER, oldUnit = 'byte', newUnit = self.config['byte_unit'])

                metric_name = '.'.join([info['device'], key])
                # io_in_progress is a point in time counter, don't derivative
                if key != 'io_in_progress':
                    metric_value = self.derivative(metric_name, value, self.MAX_VALUES[key])
                else:
                    metric_value = value;

                metrics[key] = metric_value

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
            metrics['average_queue_length']             = metrics['io_milliseconds'] / time_delta * 1000.0
            metrics['await']                            = 0
            metrics['service_time']                     = 0
            metrics['iops']                             = (metrics['reads'] + metrics['writes']) / time_delta
            metrics['io']                               = metrics['reads'] + metrics['writes']
            metrics['util_percentage']                  = 0
            metrics['concurrent_io']                    = 0

            if metrics['io'] > 0:
                rkey = 'reads_%s' % (self.config['byte_unit'])
                wkey = 'writes_%s' % (self.config['byte_unit'])
                metric_name = 'average_request_size_%s' % (self.config['byte_unit'])

                metrics[metric_name]                    = (metrics[rkey] + metrics[wkey] ) / metrics['io']
                metrics['service_time']                 = metrics['io_milliseconds'] / metrics['io']
                metrics['await']                        = metrics['io_milliseconds_weighted'] / metrics['io']
                metrics['util_percentage']              = (metrics['io'] * metrics['service_time'] / 1000.0) * 100.0

                # http://www.scribd.com/doc/15013525/Your-Disk-Array-is-Slower-Than-it-Should-Be Page 28
                metrics['concurrent_io']                = (metrics['reads_per_second'] + metrics['writes_per_second']) * (metrics['service_time'] / 1000.0)

                # Only publish when we have io figures
                for key in metrics:
                    metric_name = '.'.join([info['device'], key])
                    self.publish(metric_name, metrics[key])
