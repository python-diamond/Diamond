#!/usr/bin/python
# coding=utf-8

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import MagicMock, Mock
from mock import patch

from diamond.collector import Collector
from mountstats import MountStatsCollector

from pprint import pprint

class TestMountStatsCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('MountStatsCollector', {
            'exclude_filters': ['^/mnt/path2'],
            'interval': 10
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
        published_metrics = {
            '_mnt_path1.events.delay': 0.0,
            '_mnt_path1.bytes.serverwritebytes': 75.7,
            '_mnt_path1.xprt.tcp.backlogutil': 3509.3,
            '_mnt_path1.rpc.write.ops': 1.6
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
