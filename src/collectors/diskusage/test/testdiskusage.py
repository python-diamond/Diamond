#!/usr/bin/python
# coding=utf-8
################################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import Mock
from mock import patch
from contextlib import nested

from diamond.collector import Collector
from diskusage import DiskUsageCollector

################################################################################


class TestDiskUsageCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('DiskUsageCollector', {
            'interval': 10,
            'byte_unit': 'kilobyte'
        })

        self.collector = DiskUsageCollector(config, None)

    @patch('os.access', Mock(return_value=True))
    def test_get_disk_statistics(self):
        with nested(
            patch('__builtin__.open', Mock(
                return_value=self.getFixture('diskstats')))):

            result = self.collector.get_disk_statistics()

            open.assert_called_once_with('/proc/diskstats')

        self.assertEqual(
            sorted(result.keys()),
            [(8,  0), (8,  1), (8, 16), (8, 17), (8, 32),
                (8, 33), (8, 48), (8, 49), (9,  0)])

        return result

    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):

        with nested(
            patch('__builtin__.open', Mock(
                return_value=self.getFixture('proc_diskstats_1'))),
                patch('time.time', Mock(return_value=10))):
            self.collector.collect()

        self.assertPublishedMany(publish_mock, {})

        with nested(
            patch('__builtin__.open', Mock(
                return_value=self.getFixture('proc_diskstats_2'))),
                patch('time.time', Mock(return_value=20))):
            self.collector.collect()

        metrics = {
            'sda.average_queue_length':             0.0,
            'sda.average_request_size_kilobyte':    10.6,
            'sda.await':                            0.0,
            'sda.concurrent_io':                    0.0,
            'sda.io':                               3.0,
            'sda.io_in_progress':                   0.0,
            'sda.io_milliseconds':                  0.0,
            'sda.io_milliseconds_weighted':         0.0,
            'sda.iops':                             0.3,
            'sda.read_kilobyte_per_second':         0.0,
            'sda.read_requests_merged_per_second':  0.0,
            'sda.reads':                            0.0,
            'sda.reads_kilobyte':                   0.0,
            'sda.reads_merged':                     0.0,
            'sda.reads_milliseconds':               0.0,
            'sda.reads_per_second':                 0.0,
            'sda.service_time':                     0.0,
            'sda.util_percentage':                  0.0,
            'sda.write_kilobyte_per_second':        3.2,
            'sda.write_requests_merged_per_second': 0.5,
            'sda.writes':                           3.0,
            'sda.writes_kilobyte':                  32.0,
            'sda.writes_merged':                    5.0,
            'sda.writes_milliseconds':              0.0,
            'sda.writes_per_second':                0.3,

            'sdb.average_queue_length':             495700.0,
            'sdb.average_request_size_kilobyte':    6.3,
            'sdb.await':                            0.8,
            'sdb.concurrent_io':                    0.5,
            'sdb.io':                               9214.0,
            'sdb.io_in_progress':                   0.0,
            'sdb.io_milliseconds':                  4957.0,
            'sdb.io_milliseconds_weighted':         7492.0,
            'sdb.iops':                             921.4,
            'sdb.read_kilobyte_per_second':         1862.4,
            'sdb.read_requests_merged_per_second':  0.0,
            'sdb.reads':                            1164.0,
            'sdb.reads_kilobyte':                   18624.0,
            'sdb.reads_merged':                     0.0,
            'sdb.reads_milliseconds':               7163.0,
            'sdb.reads_per_second':                 116.4,
            'sdb.service_time':                     0.5,
            'sdb.util_percentage':                  495.7,
            'sdb.write_kilobyte_per_second':        3914.3,
            'sdb.write_requests_merged_per_second': 201.7,
            'sdb.writes':                           8050.0,
            'sdb.writes_kilobyte':                  39143.0,
            'sdb.writes_merged':                    2017.0,
            'sdb.writes_milliseconds':              337.0,
            'sdb.writes_per_second':                805.0,
        }

        self.setDocExample(self.collector.__class__.__name__, metrics)
        self.assertPublishedMany(publish_mock, metrics)

################################################################################
if __name__ == "__main__":
    unittest.main()
