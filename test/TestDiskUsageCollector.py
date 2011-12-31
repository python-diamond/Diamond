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
            'sda.write_requests_merged_per_second' : 0.05,
            'sda.read_requests_merged_per_second' : 0.0,
            'sda.reads' : 0.0,
            'sda.iops' : 0.03,
            'sda.io' : 0.3,
            'sda.io_milliseconds_weighted' : 0.0,
            'sda.writes' : 0.3,
            'sda.service_time' : 0.0,
            'sda.average_request_size_kilobyte' : 10.6666666667,
            'sda.io_milliseconds' : 0.0,
            'sda.writes_milliseconds' : 0.0,
            'sda.await' : 0.0,
            'sda.util_percentage' : 0.0,
            'sda.reads_kilobyte' : 0.0,
            'sda.read_kilobyte_per_second' : 0.0,
            'sda.writes_per_second' : 0.03,
            'sda.io_in_progress' : 0.0,
            'sda.reads_per_second' : 0.0,
            'sda.concurrent_io' : 0.0,
            'sda.writes_kilobyte' : 3.2,
            'sda.write_kilobyte_per_second' : 0.32,
            'sda.writes_merged' : 0.5,
            'sda.reads_merged' : 0.0,
            'sda.average_queue_length' : 0.0,
            'sda.reads_milliseconds' : 0.0,

            'sdb.write_requests_merged_per_second' : 20.17,
            'sdb.read_requests_merged_per_second' : 0.0,
            'sdb.reads' : 116.4,
            'sdb.iops' : 92.14,
            'sdb.io' : 921.4,
            'sdb.io_milliseconds_weighted' : 749.2,
            'sdb.writes' : 805.0,
            'sdb.service_time' : 0.54,
            'sdb.average_request_size_kilobyte' : 6.27,
            'sdb.io_milliseconds' : 495.7,
            'sdb.writes_milliseconds' : 33.7,
            'sdb.await' : 0.81,
            'sdb.util_percentage' : 49.57,
            'sdb.reads_kilobyte' : 1862.4,
            'sdb.read_kilobyte_per_second' : 186.24,
            'sdb.writes_per_second' : 80.5,
            'sdb.io_in_progress' : 33.7,
            'sdb.reads_per_second' : 11.64,
            'sdb.concurrent_io' : 0.05,
            'sdb.writes_kilobyte' : 3914.3,
            'sdb.write_kilobyte_per_second' : 391.43,
            'sdb.writes_merged' : 201.7,
            'sdb.reads_merged' : 0.0,
            'sdb.average_queue_length' : 49570.0,
            'sdb.reads_milliseconds' : 716.3,
        })

################################################################################
if __name__ == "__main__":
    unittest.main()
