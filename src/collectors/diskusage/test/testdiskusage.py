#!/usr/bin/python
# coding=utf-8
################################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import Mock
from mock import patch

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

    def test_import(self):
        self.assertTrue(DiskUsageCollector)

    @patch('os.access', Mock(return_value=True))
    def test_get_disk_statistics(self):

        patch_open = patch('__builtin__.open',
                           Mock(return_value=self.getFixture('diskstats')))

        open_mock = patch_open.start()
        result = self.collector.get_disk_statistics()
        patch_open.stop()

        open_mock.assert_called_once_with('/proc/diskstats')

        self.assertEqual(
            sorted(result.keys()),
            [(8,  0), (8,  1), (8, 16), (8, 17), (8, 32),
                (8, 33), (8, 48), (8, 49), (9,  0)])

        return result

    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):

        patch_open = patch('__builtin__.open',
                           Mock(
                            return_value=self.getFixture('proc_diskstats_1')))
        patch_time = patch('time.time', Mock(return_value=10))

        patch_open.start()
        patch_time.start()
        self.collector.collect()
        patch_open.stop()
        patch_time.stop()

        self.assertPublishedMany(publish_mock, {})

        patch_open = patch('__builtin__.open',
                           Mock(
                            return_value=self.getFixture('proc_diskstats_2')))
        patch_time = patch('time.time', Mock(return_value=20))

        patch_open.start()
        patch_time.start()
        self.collector.collect()
        patch_open.stop()
        patch_time.stop()

        metrics = self.getPickledResults('test_should_work_with_real_data.pkl')
        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_verify_supporting_vda_and_xvdb(self, publish_mock):
        patch_open = patch('__builtin__.open',
                           Mock(
                            return_value=self.getFixture(
                                'proc_diskstats_1_vda_xvdb')))
        patch_time = patch('time.time', Mock(return_value=10))

        patch_open.start()
        patch_time.start()
        self.collector.collect()
        patch_open.stop()
        patch_time.stop()

        self.assertPublishedMany(publish_mock, {})

        patch_open = patch('__builtin__.open',
                           Mock(
                            return_value=self.getFixture(
                                'proc_diskstats_2_vda_xvdb')))
        patch_time = patch('time.time', Mock(return_value=20))

        patch_open.start()
        patch_time.start()
        self.collector.collect()
        patch_open.stop()
        patch_time.stop()

        metrics = self.getPickledResults(
            'test_verify_supporting_vda_and_xvdb.pkl')
        self.assertPublishedMany(publish_mock, metrics)

    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_verify_supporting_md_dm(self, publish_mock):
        patch_open = patch('__builtin__.open',
                           Mock(
                            return_value=self.getFixture(
                                'proc_diskstats_1_md_dm')))
        patch_time = patch('time.time', Mock(return_value=10))

        patch_open.start()
        patch_time.start()
        self.collector.collect()
        patch_open.stop()
        patch_time.stop()

        self.assertPublishedMany(publish_mock, {})

        patch_open = patch('__builtin__.open',
                           Mock(
                            return_value=self.getFixture(
                                'proc_diskstats_2_md_dm')))
        patch_time = patch('time.time', Mock(return_value=20))

        patch_open.start()
        patch_time.start()
        self.collector.collect()
        patch_open.stop()
        patch_time.stop()

        metrics = self.getPickledResults('test_verify_supporting_md_dm.pkl')
        self.assertPublishedMany(publish_mock, metrics)

    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_verify_supporting_disk(self, publish_mock):
        patch_open = patch('__builtin__.open',
                           Mock(
                            return_value=self.getFixture(
                                'proc_diskstats_1_disk')))
        patch_time = patch('time.time', Mock(return_value=10))

        patch_open.start()
        patch_time.start()
        self.collector.collect()
        patch_open.stop()
        patch_time.stop()

        self.assertPublishedMany(publish_mock, {})

        patch_open = patch('__builtin__.open',
                           Mock(
                            return_value=self.getFixture(
                                'proc_diskstats_2_disk')))
        patch_time = patch('time.time', Mock(return_value=20))

        patch_open.start()
        patch_time.start()
        self.collector.collect()
        patch_open.stop()
        patch_time.stop()

        metrics = self.getPickledResults('test_verify_supporting_disk.pkl')
        self.assertPublishedMany(publish_mock, metrics)

    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_service_Time(self, publish_mock):
        patch_open = patch('__builtin__.open',
                           Mock(
                            return_value=self.getFixture(
                                'proc_diskstats_1_service_time')))
        patch_time = patch('time.time', Mock(return_value=10))

        patch_open.start()
        patch_time.start()
        self.collector.collect()
        patch_open.stop()
        patch_time.stop()

        self.assertPublishedMany(publish_mock, {})

        patch_open = patch('__builtin__.open',
                           Mock(
                            return_value=self.getFixture(
                                'proc_diskstats_2_service_time')))
        patch_time = patch('time.time', Mock(return_value=70))

        patch_open.start()
        patch_time.start()
        self.collector.collect()
        patch_open.stop()
        patch_time.stop()

        metrics = {
            'sda.write_requests_merged_per_second': 18.1666666667,
            'sda.read_requests_merged_per_second': 0.0,
            'sda.reads': 38.0,
            'sda.iops': 4.36666666667,
            'sda.io': 262.0,
            'sda.io_milliseconds_weighted': 396.0,
            'sda.read_await': 7.15789473684,
            'sda.writes': 224.0,
            'sda.service_time': 0.732824427481,
            'sda.average_request_size_kilobyte': 21.6030534351,
            'sda.io_milliseconds': 192.0,
            'sda.write_await': 0.553571428571,
            'sda.writes_milliseconds': 124.0,
            'sda.await': 1.51145038168,
            'sda.util_percentage': 19.2,
            'sda.reads_kilobyte': 696.0,
            'sda.read_kilobyte_per_second': 11.6,
            'sda.writes_per_second': 3.73333333333,
            'sda.io_in_progress': 0.0,
            'sda.reads_per_second': 0.633333333333,
            'sda.concurrent_io': 0.0032,
            'sda.writes_kilobyte': 4964.0,
            'sda.write_kilobyte_per_second': 82.7333333333,
            'sda.writes_merged': 1090.0,
            'sda.reads_merged': 0.0,
            'sda.average_queue_length': 3200.0,
            'sda.reads_milliseconds': 272.0,
            'sda5.write_requests_merged_per_second': 18.1666666667,
            'sda5.read_requests_merged_per_second': 0.0,
            'sda5.reads': 38.0,
            'sda5.iops': 3.15,
            'sda5.io': 189.0,
            'sda5.io_milliseconds_weighted': 396.0,
            'sda5.read_await': 7.15789473684,
            'sda5.writes': 151.0,
            'sda5.service_time': 1.01587301587,
            'sda5.average_request_size_kilobyte': 29.9470899471,
            'sda5.io_milliseconds': 192.0,
            'sda5.write_await': 0.82119205298,
            'sda5.writes_milliseconds': 124.0,
            'sda5.await': 2.09523809524,
            'sda5.util_percentage': 19.2,
            'sda5.reads_kilobyte': 696.0,
            'sda5.read_kilobyte_per_second': 11.6,
            'sda5.writes_per_second': 2.51666666667,
            'sda5.io_in_progress': 0.0,
            'sda5.reads_per_second': 0.633333333333,
            'sda5.concurrent_io': 0.0032,
            'sda5.writes_kilobyte': 4964.0,
            'sda5.write_kilobyte_per_second': 82.7333333333,
            'sda5.writes_merged': 1090.0,
            'sda5.reads_merged': 0.0,
            'sda5.average_queue_length': 3200.0,
            'sda5.reads_milliseconds': 272.0,
            'dm-0.write_requests_merged_per_second': 0.0,
            'dm-0.read_requests_merged_per_second': 0.0,
            'dm-0.reads': 38.0,
            'dm-0.iops': 22.2333333333,
            'dm-0.io': 1334.0,
            'dm-0.io_milliseconds_weighted': 1172.0,
            'dm-0.read_await': 7.15789473684,
            'dm-0.writes': 1296.0,
            'dm-0.service_time': 0.143928035982,
            'dm-0.average_request_size_kilobyte': 4.24287856072,
            'dm-0.io_milliseconds': 192.0,
            'dm-0.write_await': 0.694444444444,
            'dm-0.writes_milliseconds': 900.0,
            'dm-0.await': 0.87856071964,
            'dm-0.util_percentage': 19.2,
            'dm-0.reads_kilobyte': 696.0,
            'dm-0.read_kilobyte_per_second': 11.6,
            'dm-0.writes_per_second': 21.6,
            'dm-0.io_in_progress': 0.0,
            'dm-0.reads_per_second': 0.633333333333,
            'dm-0.concurrent_io': 0.0032,
            'dm-0.writes_kilobyte': 4964.0,
            'dm-0.write_kilobyte_per_second': 82.7333333333,
            'dm-0.writes_merged': 0.0,
            'dm-0.reads_merged': 0.0,
            'dm-0.average_queue_length': 3200.0,
            'dm-0.reads_milliseconds': 272.0
        }
        self.assertPublishedMany(publish_mock, metrics)


################################################################################
if __name__ == "__main__":
    unittest.main()
