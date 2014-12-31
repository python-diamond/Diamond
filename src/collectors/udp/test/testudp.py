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
from udp import UDPCollector

################################################################################


class TestUDPCollector(CollectorTestCase):
    def setUp(self, allowed_names=None):
        if not allowed_names:
            allowed_names = []
        config = get_collector_config('UDPCollector', {
            'allowed_names': allowed_names,
            'interval': 1
        })
        self.collector = UDPCollector(config, None)

    def test_import(self):
        self.assertTrue(UDPCollector)

    @patch('os.access', Mock(return_value=True))
    @patch('__builtin__.open')
    @patch.object(Collector, 'publish')
    def test_should_open_proc_net_snmp(self, publish_mock, open_mock):
        UDPCollector.PROC = ['/proc/net/snmp']
        open_mock.return_value = StringIO('')
        self.collector.collect()
        open_mock.assert_called_once_with('/proc/net/snmp')

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        self.setUp([])

        UDPCollector.PROC = [
            self.getFixturePath('proc_net_snmp_1'),
            ]
        self.collector.collect()
        self.assertPublishedMany(publish_mock, {})

        UDPCollector.PROC = [
            self.getFixturePath('proc_net_snmp_2'),
            ]
        self.collector.collect()

        metrics = {
            'InDatagrams': 352320636.0,
            'InErrors': 5.0,
            'NoPorts': 449.0,
            'OutDatagrams': 352353358.0,
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

################################################################################
if __name__ == "__main__":
    unittest.main()
