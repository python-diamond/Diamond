#!/usr/bin/python
# coding=utf-8
################################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import Mock
from mock import patch

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from diamond.collector import Collector
from soft import SoftInterruptCollector

################################################################################


class TestSoftInterruptCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('SoftInterruptCollector', {
            'interval': 1
        })

        self.collector = SoftInterruptCollector(config, None)

    def test_import(self):
        self.assertTrue(SoftInterruptCollector)

    @patch('__builtin__.open')
    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_open_proc_stat(self, publish_mock, open_mock):
        open_mock.return_value = StringIO('')
        self.collector.collect()
        open_mock.assert_called_once_with('/proc/stat', 'r')

    @patch.object(Collector, 'publish')
    def test_should_work_with_synthetic_data(self, publish_mock):
        patch_open = patch('__builtin__.open', Mock(return_value=StringIO(
            'softirq 0 0 0 0 0 0 0 0 0 0 0'
        )))

        patch_open.start()
        self.collector.collect()
        patch_open.stop()

        self.assertPublishedMany(publish_mock, {})

        patch_open = patch('__builtin__.open', Mock(return_value=StringIO(
            'softirq 55 1 2 3 4 5 6 7 8 9 10'
        )))

        patch_open.start()
        self.collector.collect()
        patch_open.stop()

        self.assertPublishedMany(publish_mock, {
            'total': 55.0,
            '0': 1,
            '1': 2,
            '2': 3,
            '3': 4,
            '4': 5,
            '5': 6,
            '6': 7,
            '7': 8,
            '8': 9,
            '9': 10,
        })

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        SoftInterruptCollector.PROC = self.getFixturePath('proc_stat_1')
        self.collector.collect()

        self.assertPublishedMany(publish_mock, {})

        SoftInterruptCollector.PROC = self.getFixturePath('proc_stat_2')
        self.collector.collect()

        metrics = {
            'total': 4971,
            '0': 0,
            '1': 1729,
            '2': 2,
            '3': 240,
            '4': 31,
            '5': 0,
            '6': 0,
            '7': 1480,
            '8': 0,
            '9': 1489,
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

################################################################################
if __name__ == "__main__":
    unittest.main()
