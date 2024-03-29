#!/usr/bin/env python
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

from ip import IPCollector

###############################################################################


class TestIPCollector(CollectorTestCase):

    def setUp(self, allowed_names=None):
        if not allowed_names:
            allowed_names = []
        config = get_collector_config('IPCollector', {
            'allowed_names': allowed_names,
            'interval': 1,
        })
        self.collector = IPCollector(config, None)

    def test_import(self):
        self.assertTrue(IPCollector)

    @patch('os.access', Mock(return_value=True))
    @patch('__builtin__.open')
    @patch('diamond.collector.Collector.publish')
    def test_should_open_proc_net_snmp(self, publish_mock, open_mock):
        IPCollector.PROC = ['/proc/net/snmp']
        open_mock.return_value = StringIO('')
        self.collector.collect_ipv4()
        open_mock.assert_called_once_with('/proc/net/snmp')

        open_mock.reset_mock()
        IPCollector.PROC6 = ['/proc/net/snmp6']
        open_mock.return_value = StringIO('')
        self.collector.collect_ipv6()
        open_mock.assert_called_once_with('/proc/net/snmp6')

    @patch('os.access', Mock(return_value=True))
    @patch('__builtin__.open')
    @patch('diamond.collector.Collector.publish')
    def test_should_work_with_synthetic_data(self, publish_mock, open_mock):
        IPCollector.PROC = ['/proc/net/snmp']
        IPCollector.PROC6 = ['/proc/net/snmp6']
        self.setUp(['A', 'C', 'A6', 'C6'])
        open_mock.side_effect = [StringIO('''
Ip: A B C
Ip: 0 0 0
'''.strip()), StringIO('''
A6    0
B6    0
C6    0
'''.strip())]

        self.collector.collect()

        open_mock.side_effect = [StringIO('''
Ip: A B C
Ip: 0 1 2
'''.strip()), StringIO('''
A6    0
B6    1
C6    2
'''.strip())]

        publish_mock.call_args_list = []

        self.collector.collect()

        self.assertEqual(len(publish_mock.call_args_list), 4)

        metrics = {
            'A': 0,
            'C': 2,
            'A6': 0,
            'C6': 2
        }

        self.assertPublishedMany(publish_mock, metrics)

    @patch('diamond.collector.Collector.publish')
    def test_should_work_with_real_data(self, publish_mock):
        self.setUp(['InDiscards', 'InReceives', 'OutDiscards', 'OutRequests',
                    'Ip6InDiscards', 'Ip6InReceives', 'Ip6OutDiscards',
                    'Ip6OutRequests'])

        IPCollector.PROC = [self.getFixturePath('proc_net_snmp_1')]
        IPCollector.PROC6 = [self.getFixturePath('proc_net_snmp6_1')]
        self.collector.collect()
        self.assertPublishedMany(publish_mock, {})

        IPCollector.PROC = [self.getFixturePath('proc_net_snmp_2')]
        IPCollector.PROC6 = [self.getFixturePath('proc_net_snmp6_2')]
        self.collector.collect()

        metrics = {
            'InDiscards': 0,
            'InReceives': 2,
            'OutDiscards': 0,
            'OutRequests': 1,
            'Ip6InReceives': 2,
            'Ip6InDiscards': 0,
            'Ip6OutDiscards': 4,
            'Ip6OutRequests': 1
        }

        self.assertPublishedMany(publish_mock, metrics)

    @patch('diamond.collector.Collector.publish')
    def test_should_work_with_all_data(self, publish_mock):
        metrics = {
            'Forwarding':       2,
            'DefaultTTL':       64,
            'InReceives':       2,
            'InHdrErrors':      0,
            'InAddrErrors':     0,
            'ForwDatagrams':    0,
            'InUnknownProtos':  0,
            'InDiscards':       0,
            'InDelivers':       2,
            'OutRequests':      1,
            'OutDiscards':      0,
            'OutNoRoutes':      0,
            'ReasmTimeout':     0,
            'ReasmReqds':       0,
            'ReasmOKs':         0,
            'ReasmFails':       0,
            'FragOKs':          0,
            'FragFails':        0,
            'FragCreates':      0,
        }

        self.setUp(allowed_names=metrics.keys())

        IPCollector.PROC = [
            self.getFixturePath('proc_net_snmp_1'),
        ]
        IPCollector.PROC6 = [self.getFixturePath('proc_net_snmp6_1')]

        self.collector.collect()
        self.assertPublishedMany(publish_mock, {})

        IPCollector.PROC = [
            self.getFixturePath('proc_net_snmp_2'),
        ]
        IPCollector.PROC6 = [self.getFixturePath('proc_net_snmp6_1')]

        self.collector.collect()

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

###############################################################################
if __name__ == '__main__':
    unittest.main()
