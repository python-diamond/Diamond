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
            'sector_size': '512',
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

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_verify_supporting_vda_and_xvdb(self, publish_mock):

        with nested(
            patch('__builtin__.open', Mock(
                return_value=self.getFixture('proc_diskstats_1_vda_xvdb'))),
                patch('time.time', Mock(return_value=10))):
            self.collector.collect()

        self.assertPublishedMany(publish_mock, {})

        with nested(
            patch('__builtin__.open', Mock(
                return_value=self.getFixture('proc_diskstats_2_vda_xvdb'))),
                patch('time.time', Mock(return_value=20))):
            self.collector.collect()

        metrics = {
            'vda.average_queue_length':             0.0,
            'vda.average_request_size_kilobyte':    10.6,
            'vda.await':                            0.0,
            'vda.concurrent_io':                    0.0,
            'vda.io':                               3.0,
            'vda.io_in_progress':                   0.0,
            'vda.io_milliseconds':                  0.0,
            'vda.io_milliseconds_weighted':         0.0,
            'vda.iops':                             0.3,
            'vda.read_kilobyte_per_second':         0.0,
            'vda.read_requests_merged_per_second':  0.0,
            'vda.reads':                            0.0,
            'vda.reads_kilobyte':                   0.0,
            'vda.reads_merged':                     0.0,
            'vda.reads_milliseconds':               0.0,
            'vda.reads_per_second':                 0.0,
            'vda.service_time':                     0.0,
            'vda.util_percentage':                  0.0,
            'vda.write_kilobyte_per_second':        3.2,
            'vda.write_requests_merged_per_second': 0.5,
            'vda.writes':                           3.0,
            'vda.writes_kilobyte':                  32.0,
            'vda.writes_merged':                    5.0,
            'vda.writes_milliseconds':              0.0,
            'vda.writes_per_second':                0.3,

            'xvdb.average_queue_length':             495700.0,
            'xvdb.average_request_size_kilobyte':    6.3,
            'xvdb.await':                            0.8,
            'xvdb.concurrent_io':                    0.5,
            'xvdb.io':                               9214.0,
            'xvdb.io_in_progress':                   0.0,
            'xvdb.io_milliseconds':                  4957.0,
            'xvdb.io_milliseconds_weighted':         7492.0,
            'xvdb.iops':                             921.4,
            'xvdb.read_kilobyte_per_second':         1862.4,
            'xvdb.read_requests_merged_per_second':  0.0,
            'xvdb.reads':                            1164.0,
            'xvdb.reads_kilobyte':                   18624.0,
            'xvdb.reads_merged':                     0.0,
            'xvdb.reads_milliseconds':               7163.0,
            'xvdb.reads_per_second':                 116.4,
            'xvdb.service_time':                     0.5,
            'xvdb.util_percentage':                  495.7,
            'xvdb.write_kilobyte_per_second':        3914.3,
            'xvdb.write_requests_merged_per_second': 201.7,
            'xvdb.writes':                           8050.0,
            'xvdb.writes_kilobyte':                  39143.0,
            'xvdb.writes_merged':                    2017.0,
            'xvdb.writes_milliseconds':              337.0,
            'xvdb.writes_per_second':                805.0,
        }

        self.assertPublishedMany(publish_mock, metrics)


    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_verify_supporting_md_dm(self, publish_mock):

        with nested(
            patch('__builtin__.open', Mock(
                return_value=self.getFixture('proc_diskstats_1_md_dm'))),
                patch('time.time', Mock(return_value=10))):
            self.collector.collect()

        self.assertPublishedMany(publish_mock, {})

        with nested(
            patch('__builtin__.open', Mock(
                return_value=self.getFixture('proc_diskstats_2_md_dm'))),
                patch('time.time', Mock(return_value=20))):
            self.collector.collect()

        metrics = {
            'md0.average_queue_length':             0.0,
            'md0.average_request_size_kilobyte':    10.6,
            'md0.await':                            0.0,
            'md0.concurrent_io':                    0.0,
            'md0.io':                               3.0,
            'md0.io_in_progress':                   0.0,
            'md0.io_milliseconds':                  0.0,
            'md0.io_milliseconds_weighted':         0.0,
            'md0.iops':                             0.3,
            'md0.read_kilobyte_per_second':         0.0,
            'md0.read_requests_merged_per_second':  0.0,
            'md0.reads':                            0.0,
            'md0.reads_kilobyte':                   0.0,
            'md0.reads_merged':                     0.0,
            'md0.reads_milliseconds':               0.0,
            'md0.reads_per_second':                 0.0,
            'md0.service_time':                     0.0,
            'md0.util_percentage':                  0.0,
            'md0.write_kilobyte_per_second':        3.2,
            'md0.write_requests_merged_per_second': 0.5,
            'md0.writes':                           3.0,
            'md0.writes_kilobyte':                  32.0,
            'md0.writes_merged':                    5.0,
            'md0.writes_milliseconds':              0.0,
            'md0.writes_per_second':                0.3,

            'dm-0.average_queue_length':             495700.0,
            'dm-0.average_request_size_kilobyte':    6.3,
            'dm-0.await':                            0.8,
            'dm-0.concurrent_io':                    0.5,
            'dm-0.io':                               9214.0,
            'dm-0.io_in_progress':                   0.0,
            'dm-0.io_milliseconds':                  4957.0,
            'dm-0.io_milliseconds_weighted':         7491.0,
            'dm-0.iops':                             921.4,
            'dm-0.read_kilobyte_per_second':         1862.4,
            'dm-0.read_requests_merged_per_second':  0.0,
            'dm-0.reads':                            1164.0,
            'dm-0.reads_kilobyte':                   18624.0,
            'dm-0.reads_merged':                     0.0,
            'dm-0.reads_milliseconds':               7163.0,
            'dm-0.reads_per_second':                 116.4,
            'dm-0.service_time':                     0.5,
            'dm-0.util_percentage':                  495.7,
            'dm-0.write_kilobyte_per_second':        3914.3,
            'dm-0.write_requests_merged_per_second': 201.7,
            'dm-0.writes':                           8050.0,
            'dm-0.writes_kilobyte':                  39143.0,
            'dm-0.writes_merged':                    2017.0,
            'dm-0.writes_milliseconds':              337.0,
            'dm-0.writes_per_second':                805.0,
        }

        self.assertPublishedMany(publish_mock, metrics)


    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_verify_supporting_disk(self, publish_mock):

        with nested(
            patch('__builtin__.open', Mock(
                return_value=self.getFixture('proc_diskstats_1_disk'))),
                patch('time.time', Mock(return_value=10))):
            self.collector.collect()

        self.assertPublishedMany(publish_mock, {})

        with nested(
            patch('__builtin__.open', Mock(
                return_value=self.getFixture('proc_diskstats_2_disk'))),
                patch('time.time', Mock(return_value=20))):
            self.collector.collect()

        metrics = {
            'disk1.average_queue_length':             0.0,
            'disk1.average_request_size_kilobyte':    10.6,
            'disk1.await':                            0.0,
            'disk1.concurrent_io':                    0.0,
            'disk1.io':                               3.0,
            'disk1.io_in_progress':                   0.0,
            'disk1.io_milliseconds':                  0.0,
            'disk1.io_milliseconds_weighted':         0.0,
            'disk1.iops':                             0.3,
            'disk1.read_kilobyte_per_second':         0.0,
            'disk1.read_requests_merged_per_second':  0.0,
            'disk1.reads':                            0.0,
            'disk1.reads_kilobyte':                   0.0,
            'disk1.reads_merged':                     0.0,
            'disk1.reads_milliseconds':               0.0,
            'disk1.reads_per_second':                 0.0,
            'disk1.service_time':                     0.0,
            'disk1.util_percentage':                  0.0,
            'disk1.write_kilobyte_per_second':        3.2,
            'disk1.write_requests_merged_per_second': 0.5,
            'disk1.writes':                           3.0,
            'disk1.writes_kilobyte':                  32.0,
            'disk1.writes_merged':                    5.0,
            'disk1.writes_milliseconds':              0.0,
            'disk1.writes_per_second':                0.3,
        }

        self.assertPublishedMany(publish_mock, metrics)


################################################################################
if __name__ == "__main__":
    unittest.main()
