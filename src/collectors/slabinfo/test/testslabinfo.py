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
from slabinfo import SlabInfoCollector

################################################################################


class TestSlabInfoCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('SlabInfoCollector', {
            'interval': 1
        })

        self.collector = SlabInfoCollector(config, None)

    def test_import(self):
        self.assertTrue(SlabInfoCollector)

    @patch('__builtin__.open')
    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_open_proc_stat(self, publish_mock, open_mock):
        open_mock.return_value = StringIO('')
        self.collector.collect()
        open_mock.assert_called_once_with('/proc/slabinfo', 'r')

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        SlabInfoCollector.PROC = self.getFixturePath('slabinfo')
        self.collector.collect()

        metrics = self.getPickledResults('expected.pkl')

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

################################################################################
if __name__ == "__main__":
    unittest.main()
