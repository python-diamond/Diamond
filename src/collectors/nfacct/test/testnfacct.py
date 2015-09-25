#!/usr/bin/python
# coding=utf-8
##########################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import Mock
from mock import patch

from diamond.collector import Collector
from nfacct import NetfilterAccountingCollector

##########################################################################


class TestNetfilterAccountingCollector(CollectorTestCase):

    def setUp(self):
        config = get_collector_config('NetfilterAccountingCollector', {
            'interval': 10,
            'bin': 'true',
        })

        self.collector = NetfilterAccountingCollector(config, None)

    def test_import(self):
        self.assertTrue(NetfilterAccountingCollector)

    @patch.object(Collector, 'publish')
    def test_no_counters(self, publish_mock):
        patch_communicate = patch(
            'subprocess.Popen.communicate',
            Mock(return_value=('', '')))
        patch_communicate.start()
        self.collector.collect()
        patch_communicate.stop()

        self.assertPublishedMany(publish_mock, {})

    @patch.object(Collector, 'publish')
    def test_counters(self, publish_mock):
        patch_communicate = patch(
            'subprocess.Popen.communicate',
            Mock(return_value=(self.getFixture('nfacct').getvalue(), '')))
        patch_communicate.start()
        self.collector.collect()
        patch_communicate.stop()

        self.assertPublishedMany(publish_mock, {
            'Tcp.pkts': 3,
            'Tcp.bytes': 300,
            'Udp.pkts': 0,
            'Udp.bytes': 0,
            'Tcp.Incoming.pkts': 1,
            'Tcp.Incoming.bytes': 100,
            'Tcp.Outgoing.pkts': 2,
            'Tcp.Outgoing.bytes': 200,
        })


##########################################################################
if __name__ == "__main__":
    unittest.main()
