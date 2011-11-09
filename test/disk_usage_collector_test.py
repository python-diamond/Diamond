#!/usr/bin/python
################################################################################

from common import *

from diamond.collector import Collector
from disk_usage_collector import DiskUsageCollector

import disk

################################################################################

class TestDiskUsageCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('DiskUsageCollector', {
            'interval': 10
        })

        self.collector = DiskUsageCollector(config, None)

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        with nested(
            patch('os.stat'),
            patch('os.major', return_value = 9),
            patch('os.minor', return_value = 0),
            patch('__builtin__.open', return_value = get_fixture('proc_mounts'))
        ):
            file_systems = disk.get_file_systems()

        with patch('__builtin__.open', return_value = get_fixture('proc_diskstats_1')):
            disk_statistics_1 = disk.get_disk_statistics()

        with patch('__builtin__.open', return_value = get_fixture('proc_diskstats_2')):
            disk_statistics_2 = disk.get_disk_statistics()

        with nested(
            patch('disk.get_file_systems', return_value = file_systems),
            patch('disk.get_disk_statistics', return_value = disk_statistics_1)
        ):
            self.collector.collect()

        self.assertPublishedMany(publish_mock, {})

        with nested(
            patch('disk.get_file_systems', return_value = file_systems),
            patch('disk.get_disk_statistics', return_value = disk_statistics_2)
        ):
            self.collector.collect()

        self.assertPublishedMany(publish_mock, {
            'sda.reads' : 0.5,
            'sda.reads_merged' : 0.6,
            'sda.reads_kilobytes' : 4.4,
            'sda.reads_milliseconds' : 4.0,
            'sda.writes' : 3.4,
            'sda.writes_merged' : 1.3,
            'sda.writes_kilobytes' : 18.8,
            'sda.writes_milliseconds' : 10.0,
            'sda.io_milliseconds' : 9.0,
            'sda.weighted_io_milliseconds' : 14.0,
            'md0.reads' : 0.0,
            'md0.reads_merged' : 0.0,
            'md0.reads_kilobytes' : 0.0,
            'md0.reads_milliseconds' : 0.0,
            'md0.writes' : 8.6,
            'md0.writes_merged' : 0.0,
            'md0.writes_kilobytes' : 34.4,
            'md0.writes_milliseconds' : 0.0,
            'md0.io_milliseconds' : 0.0,
            'md0.weighted_io_milliseconds' : 0.0,
        })

################################################################################
if __name__ == "__main__":
    unittest.main()
