#!/usr/bin/python
# coding=utf-8
###############################################################################

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
from vmstat import VMStatCollector

###############################################################################


class TestVMStatCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('VMStatCollector', {
            'interval': 10
        })

        self.collector = VMStatCollector(config, None)

    def test_import(self):
        self.assertTrue(VMStatCollector)

    @patch('__builtin__.open')
    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_open_proc_vmstat(self, publish_mock, open_mock):
        open_mock.return_value = StringIO('')
        self.collector.collect()
        open_mock.assert_called_once_with('/proc/vmstat')

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        VMStatCollector.PROC = self.getFixturePath('proc_vmstat_1')
        self.collector.collect()

        self.assertPublishedMany(publish_mock, {})

        VMStatCollector.PROC = self.getFixturePath('proc_vmstat_2')
        self.collector.collect()

        metrics = {
            'pgpgin': 0.0,
            'pgpgout': 9.2,
            'pswpin': 0.0,
            'pswpout': 0.0,
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)


###############################################################################
if __name__ == "__main__":
    unittest.main()
