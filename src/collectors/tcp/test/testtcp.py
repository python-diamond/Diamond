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
from tcp import TCPCollector

################################################################################


class TestTCPCollector(CollectorTestCase):
    def setUp(self, allowed_names=None):
        if not allowed_names:
            allowed_names = []
        config = get_collector_config('TCPCollector', {
            'allowed_names': allowed_names,
            'interval': 1
        })
        self.collector = TCPCollector(config, None)

    @patch('os.access', Mock(return_value=True))
    @patch('__builtin__.open')
    @patch.object(Collector, 'publish')
    def test_should_open_proc_net_netstat(self, publish_mock, open_mock):
        open_mock.return_value = StringIO('')
        self.collector.collect()
        open_mock.assert_called_once_with('/proc/net/netstat')

    @patch('__builtin__.open')
    @patch.object(Collector, 'publish')
    def test_should_work_with_synthetic_data(self, publish_mock, open_mock):
        self.setUp(['A', 'C'])
        open_mock.return_value = StringIO('''
TcpExt: A B C
TcpExt: 0 0 0
'''.strip())

        self.collector.collect()
        self.assertPublishedMany(publish_mock, {})

        open_mock.return_value = StringIO('''
TcpExt: A B C
TcpExt: 0 1 2
'''.strip())

        self.collector.collect()

        self.assertEqual(len(publish_mock.call_args_list), 2)
        self.assertEqual(publish_mock.call_args_list, [
            (('A', 0.0, 0), {}),
            (('C', 2.0, 0), {})
        ])

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        self.setUp(['ListenOverflows', 'ListenDrops', 'TCPLoss', 'TCPTimeouts'])

        TCPCollector.PROC = self.getFixturePath('proc_net_netstat')
        self.collector.collect()
        self.assertPublishedMany(publish_mock, {})

        TCPCollector.PROC = self.getFixturePath('proc_net_netstat_2')
        self.collector.collect()

        metrics = {
            'ListenOverflows': 0,
            'ListenDrops': 0,
            'TCPLoss': 188,
            'TCPTimeouts': 15265
        }

        self.setDocExample(self.collector.__class__.__name__, metrics)
        self.assertPublishedMany(publish_mock, metrics)

################################################################################
if __name__ == "__main__":
    unittest.main()
