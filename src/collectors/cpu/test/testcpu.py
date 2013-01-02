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
    StringIO  # workaround for pyflakes issue #13
except ImportError:
    from StringIO import StringIO

from diamond.collector import Collector
from cpu import CPUCollector

################################################################################


class TestCPUCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('CPUCollector', {
            'interval': 10
        })

        self.collector = CPUCollector(config, None)

    def test_import(self):
        self.assertTrue(CPUCollector)

    @patch('__builtin__.open')
    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_open_proc_stat(self, publish_mock, open_mock):
        open_mock.return_value = StringIO('')
        self.collector.collect()
        open_mock.assert_called_once_with('/proc/stat')

    @patch.object(Collector, 'publish')
    def test_should_work_with_synthetic_data(self, publish_mock):
        patch_open = patch('__builtin__.open', Mock(return_value=StringIO(
            'cpu 100 200 300 400 500 0 0 0 0 0')))

        patch_open.start()
        self.collector.collect()
        patch_open.stop()

        self.assertPublishedMany(publish_mock, {})

        patch_open = patch('__builtin__.open', Mock(return_value=StringIO(
            'cpu 110 220 330 440 550 0 0 0 0 0')))

        patch_open.start()
        self.collector.collect()
        patch_open.stop()

        self.assertPublishedMany(publish_mock, {
            'total.idle': 4.0,
            'total.iowait': 5.0,
            'total.nice': 2.0,
            'total.system': 3.0,
            'total.user': 1.0
        })

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        CPUCollector.PROC = self.getFixturePath('proc_stat_1')
        self.collector.collect()

        self.assertPublishedMany(publish_mock, {})

        CPUCollector.PROC = self.getFixturePath('proc_stat_2')
        self.collector.collect()

        metrics = {
            'total.idle': 2440.8,
            'total.iowait': 0.2,
            'total.nice': 0.0,
            'total.system': 0.2,
            'total.user': 0.4
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

    @patch.object(Collector, 'publish')
    def test_should_work_with_ec2_data(self, publish_mock):
        self.collector.config['interval'] = 30
        patch_open = patch('os.path.isdir', Mock(return_value=True))
        patch_open.start()

        CPUCollector.PROC = self.getFixturePath('ec2_stat_1')
        self.collector.collect()

        self.assertPublishedMany(publish_mock, {})

        CPUCollector.PROC = self.getFixturePath('ec2_stat_2')
        self.collector.collect()

        patch_open.stop()

        metrics = {
            'total.idle': 68.4,
            'total.iowait': 0.6,
            'total.nice': 0.0,
            'total.system': 13.7,
            'total.user': 16.666666666666668
        }

        self.assertPublishedMany(publish_mock, metrics)

################################################################################
if __name__ == "__main__":
    unittest.main()
