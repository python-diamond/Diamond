#!/usr/bin/python
################################################################################

from common import *

from diamond.collector import Collector
from DiskUsageCollector import DiskUsageCollector

import disk

################################################################################

class TestDiskUsageCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('DiskUsageCollector', {
            'interval'  : 10,
            'byte_unit' : 'kilobyte'
        })

        self.collector = DiskUsageCollector(config, None)

    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        with nested(
            patch('os.stat'),
            patch('os.major', Mock(return_value = 9)),
            patch('os.minor', Mock(return_value = 0)),
            patch('__builtin__.open', Mock(return_value = get_fixture('proc_mounts')))
        ):
            file_systems = disk.get_file_systems()

        with patch('__builtin__.open', Mock(return_value = get_fixture('proc_diskstats_1'))):
            disk_statistics_1 = disk.get_disk_statistics()

        with patch('__builtin__.open', Mock(return_value = get_fixture('proc_diskstats_2'))):
            disk_statistics_2 = disk.get_disk_statistics()

        with nested(
            patch('disk.get_file_systems', Mock(return_value = file_systems)),
            patch('disk.get_disk_statistics', Mock(return_value = disk_statistics_1))
        ):
            self.collector.collect()

        self.assertPublishedMany(publish_mock, {})

        with nested(
            patch('disk.get_file_systems', Mock(return_value = file_systems)),
            patch('disk.get_disk_statistics', Mock(return_value = disk_statistics_2))
        ):
            self.collector.collect()

        self.assertPublishedMany(publish_mock, {
            'sda.write_requests_merged_per_second' : 0.13,
            'sda.read_requests_merged_per_second' : 0.06,
            'sda.reads' : 0.5,
            'sda.iops' : 0.39,
            'sda.io' : 3.9,
            'sda.io_milliseconds_weighted' : 14.0,
            'sda.writes' : 3.4,
            'sda.service_time' : 2.30769230769,
            'sda.average_request_size_kilobyte' : 5.94871794872,
            'sda.io_milliseconds' : 9.0,
            'sda.writes_milliseconds' : 10.0,
            'sda.await' : 3.58974358974,
            'sda.util_percentage' : 0.09,
            'sda.reads_kilobyte' : 4.4,
            'sda.read_kilobyte_per_second' : 0.44,
            'sda.writes_per_second' : 0.34,
            'sda.io_in_progress' : 0.0,
            'sda.reads_per_second' : 0.05,
            'sda.concurrent_io' : 0.0,
            'sda.writes_kilobyte' : 18.8,
            'sda.write_kilobyte_per_second' : 1.88,
            'sda.writes_merged' : 1.3,
            'sda.reads_merged' : 0.6,
            'sda.average_queue_length' : 900.0,
            'sda.reads_milliseconds' : 4.0,

            'sdb.write_requests_merged_per_second' : 0.13,
            'sdb.read_requests_merged_per_second' : 0.16,
            'sdb.reads' : 1.1,
            'sdb.iops' : 0.38,
            'sdb.io' : 3.8,
            'sdb.io_milliseconds_weighted' : 21.0,
            'sdb.writes' : 2.7,
            'sdb.service_time' : 2.10526315789,
            'sdb.average_request_size_kilobyte' : 7.15789473684,
            'sdb.io_milliseconds' : 8.0,
            'sdb.writes_milliseconds' : 6.0,
            'sdb.await' : 5.52631578947,
            'sdb.util_percentage' : 0.08,
            'sdb.reads_kilobyte' : 10.8,
            'sdb.read_kilobyte_per_second' : 1.08,
            'sdb.writes_per_second' : 0.27,
            'sdb.io_in_progress' : 0.0,
            'sdb.reads_per_second' : 0.11,
            'sdb.concurrent_io' : 0.0,
            'sdb.writes_kilobyte' : 16.4,
            'sdb.write_kilobyte_per_second' : 1.64,
            'sdb.writes_merged' : 1.3,
            'sdb.reads_merged' : 1.6,
            'sdb.average_queue_length' : 800.0,
            'sdb.reads_milliseconds' : 15.0,

            'sdc.write_requests_merged_per_second' : 0.23,
            'sdc.read_requests_merged_per_second' : 0.07,
            'sdc.reads' : 0.7,
            'sdc.iops' : 0.34,
            'sdc.io' : 3.4,
            'sdc.io_milliseconds_weighted' : 20.0,
            'sdc.writes' : 2.7,
            'sdc.service_time' : 2.94117647059,
            'sdc.average_request_size_kilobyte' : 7.52941176471,
            'sdc.io_milliseconds' : 10.0,
            'sdc.writes_milliseconds' : 9.0,
            'sdc.await' : 5.88235294118,
            'sdc.util_percentage' : 0.1,
            'sdc.reads_kilobyte' : 5.6,
            'sdc.read_kilobyte_per_second' : 0.56,
            'sdc.writes_per_second' : 0.27,
            'sdc.io_in_progress' : 0.0,
            'sdc.reads_per_second' : 0.07,
            'sdc.concurrent_io' : 0.0,
            'sdc.writes_kilobyte' : 20.0,
            'sdc.write_kilobyte_per_second' : 2.0,
            'sdc.writes_merged' : 2.3,
            'sdc.reads_merged' : 0.7,
            'sdc.average_queue_length' : 1000.0,
            'sdc.reads_milliseconds' : 11.0,

            'sdd.write_requests_merged_per_second' : 0.35,
            'sdd.read_requests_merged_per_second' : 0.04,
            'sdd.reads' : 0.8,
            'sdd.iops' : 0.4,
            'sdd.io' : 4.0,
            'sdd.io_milliseconds_weighted' : 20.0,
            'sdd.writes' : 3.2,
            'sdd.service_time' : 2.25,
            'sdd.average_request_size_kilobyte' : 8.0,
            'sdd.io_milliseconds' : 9.0,
            'sdd.writes_milliseconds' : 5.0,
            'sdd.await' : 5.0,
            'sdd.util_percentage' : 0.09,
            'sdd.reads_kilobyte' : 4.8,
            'sdd.read_kilobyte_per_second' : 0.48,
            'sdd.writes_per_second' : 0.32,
            'sdd.io_in_progress' : 0.0,
            'sdd.reads_per_second' : 0.08,
            'sdd.concurrent_io' : 0.0,
            'sdd.writes_kilobyte' : 27.2,
            'sdd.write_kilobyte_per_second' : 2.72,
            'sdd.writes_merged' : 3.5,
            'sdd.reads_merged' : 0.4,
            'sdd.average_queue_length' : 900.0,
            'sdd.reads_milliseconds' : 15.0,

            'md0.write_requests_merged_per_second' : 0.0,
            'md0.read_requests_merged_per_second' : 0.0,
            'md0.reads' : 0.0,
            'md0.iops' : 0.86,
            'md0.io' : 8.6,
            'md0.io_milliseconds_weighted' : 0.0,
            'md0.writes' : 8.6,
            'md0.service_time' : 0.0,
            'md0.average_request_size_kilobyte' : 4.0,
            'md0.io_milliseconds' : 0.0,
            'md0.writes_milliseconds' : 0.0,
            'md0.await' : 0.0,
            'md0.util_percentage' : 0.0,
            'md0.reads_kilobyte' : 0.0,
            'md0.read_kilobyte_per_second' : 0.0,
            'md0.writes_per_second' : 0.86,
            'md0.io_in_progress' : 0.0,
            'md0.reads_per_second' : 0.0,
            'md0.concurrent_io' : 0.0,
            'md0.writes_kilobyte' : 34.4,
            'md0.write_kilobyte_per_second' : 3.44,
            'md0.writes_merged' : 0.0,
            'md0.reads_merged' : 0.0,
            'md0.average_queue_length' : 0.0,
            'md0.reads_milliseconds' : 0.0,
        })

################################################################################
if __name__ == "__main__":
    unittest.main()
