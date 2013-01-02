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
from loadavg import LoadAverageCollector

################################################################################


class TestLoadAverageCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('LoadAverageCollector', {
            'interval': 10
        })

        self.collector = LoadAverageCollector(config, None)

    def test_import(self):
        self.assertTrue(LoadAverageCollector)

    @patch('__builtin__.open')
    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_open_proc_loadavg(self, publish_mock, open_mock):
        open_mock.return_value = StringIO('')
        self.collector.collect()
        open_mock.assert_called_once_with('/proc/loadavg')

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        LoadAverageCollector.PROC = self.getFixturePath('proc_loadavg')
        self.collector.collect()

        metrics = {
            '01': (0.00, 2),
            '05': (0.32, 2),
            '15': (0.56, 2),
            'processes_running': 1,
            'processes_total': 235
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

################################################################################
if __name__ == "__main__":
    unittest.main()
