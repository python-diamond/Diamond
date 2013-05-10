#!/usr/bin/python
# coding=utf-8

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import MagicMock, Mock
from mock import patch

from diamond.collector import Collector
from mountstats import MountStatsCollector


class TestMountStatsCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('MountStatsCollector', {
            'exclude_filters': ['^/mnt/path2'],
            'interval': 1
        })

        self.collector = MountStatsCollector(config, None)

    def test_import(self):
        self.assertTrue(MountStatsCollector)

    @patch('__builtin__.open')
    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_open_mountstats(self, publish_mock, open_mock):
        open_mock.return_value = MagicMock()
        self.collector.collect()
        open_mock.assert_called_once_with(self.collector.MOUNTSTATS)

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        # Test the first and last metric of each type
        published_metrics = {
            '_mnt_path1.events.inoderevalidates': 27110.0,
            '_mnt_path1.events.delay': 0.0,
            '_mnt_path1.bytes.normalreadbytes': 1424269.0,
            '_mnt_path1.bytes.serverwritebytes': 69460.0,
            '_mnt_path1.xprt.tcp.port': 0.0,
            '_mnt_path1.xprt.tcp.backlogutil': 11896527.0,
            '_mnt_path1.rpc.access.ops': 2988.0,
            '_mnt_path1.rpc.write.ops': 16.0
        }

        unpublished_metrics = {
            '_mnt_path2.events.delay': 0.0
        }

        self.collector.MOUNTSTATS = self.getFixturePath('mountstats_1')
        self.collector.collect()
        self.assertPublishedMany(publish_mock, {})

        self.collector.MOUNTSTATS = self.getFixturePath('mountstats_2')
        self.collector.collect()
        self.assertPublishedMany(publish_mock, published_metrics)
        self.assertUnpublishedMany(publish_mock, unpublished_metrics)

if __name__ == "__main__":
    unittest.main()
