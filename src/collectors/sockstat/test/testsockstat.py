#!/usr/bin/python
# coding=utf-8
##########################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from test import Mock
from test import patch
from test import call
from test import BUILTIN_OPEN

from collections import Iterator
from diamond.collector import Collector
from sockstat import SockstatCollector
import sys

##########################################################################


class TestSockstatCollector(CollectorTestCase):

    def setUp(self):
        config = get_collector_config('SockstatCollector', {
            'interval': 10
        })

        self.collector = SockstatCollector(config, None)

    def test_import(self):
        self.assertTrue(SockstatCollector)

    @patch(BUILTIN_OPEN)
    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_open_proc_net_sockstat(self, publish_mock, open_mock):
        class KlassPy2(Iterator):
            def close(self):
                pass

            def next(self):
                raise StopIteration()

        class KlassPy3(Iterator):
            def close(self):
                pass

            def __next__(self):
                raise StopIteration()
        # py2.6x does not support the namedtuple .major
        if sys.version_info[0] == 2:
            open_mock.return_value = KlassPy2()
        else:
            open_mock.return_value = KlassPy3()
        self.collector.collect()
        calls = [call('/proc/net/sockstat'), call('/proc/net/sockstat6')]
        open_mock.assert_has_calls(calls)

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        SockstatCollector.PROCS = [self.getFixturePath('proc_net_sockstat'),
                                   self.getFixturePath('proc_net_sockstat6')]
        self.collector.collect()

        metrics = {
            'used': 118,
            'tcp_inuse': 61,
            'tcp_orphan': 0,
            'tcp_tw': 1,
            'tcp_alloc': 13,
            'tcp_mem': 1,
            'udp_inuse': 6,
            'udp_mem': 0
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

##########################################################################
if __name__ == "__main__":
    unittest.main()
