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
from proc import ProcessStatCollector

################################################################################


class TestProcessStatCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('ProcessStatCollector', {
            'interval': 1
        })

        self.collector = ProcessStatCollector(config, None)

    def test_import(self):
        self.assertTrue(ProcessStatCollector)

    @patch('__builtin__.open')
    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_open_proc_stat(self, publish_mock, open_mock):
        open_mock.return_value = StringIO('')
        self.collector.collect()
        open_mock.assert_called_once_with('/proc/stat', 'r')

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        ProcessStatCollector.PROC = self.getFixturePath('proc_stat_1')
        self.collector.collect()

        self.assertPublishedMany(publish_mock, {})

        ProcessStatCollector.PROC = self.getFixturePath('proc_stat_2')
        self.collector.collect()

        metrics = {
            'ctxt': 0,
            'btime': 1319181102,
            'processes': 0,
            'procs_running': 1,
            'procs_blocked': 0,
            'ctxt': 1791,
            'btime': 1319181102,
            'processes': 2,
            'procs_running': 1,
            'procs_blocked': 0,
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

################################################################################
if __name__ == "__main__":
    unittest.main()
