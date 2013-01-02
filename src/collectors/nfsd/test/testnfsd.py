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
from nfsd import NfsdCollector

################################################################################


class TestNfsdCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('NfsdCollector', {
            'interval': 1
        })

        self.collector = NfsdCollector(config, None)

    def test_import(self):
        self.assertTrue(NfsdCollector)

    @patch('__builtin__.open')
    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_open_proc_stat(self, publish_mock, open_mock):
        open_mock.return_value = StringIO('')
        self.collector.collect()
        open_mock.assert_called_once_with('/proc/net/rpc/nfsd')

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        NfsdCollector.PROC = self.getFixturePath('proc_nfsd_1')
        self.collector.collect()

        self.assertPublishedMany(publish_mock, {})

        NfsdCollector.PROC = self.getFixturePath('proc_nfsd_2')
        self.collector.collect()

        metrics = {
            '.input_output.bytes-read': 3139369493.0,
            '.input_output.bytes-written': 15691669.0,
            '.net.cnt': 14564086.0,
            '.net.tcpcnt': 14562696.0,
            '.net.tcpconn': 30773.0,
            '.read-ahead.10-pct': 8751152.0,
            '.read-ahead.cache-size': 32.0,
            '.read-ahead.not-found': 18612.0,
            '.reply_cache.misses': 71080.0,
            '.reply_cache.nocache': 14491982.0,
            '.rpc.cnt': 14563007.0,
            '.threads.10-20-pct': 22163.0,
            '.threads.100-pct': 22111.0,
            '.threads.20-30-pct': 8448.0,
            '.threads.30-40-pct': 1642.0,
            '.threads.50-60-pct': 5072.0,
            '.threads.60-70-pct': 1210.0,
            '.threads.70-80-pct': 3889.0,
            '.threads.80-90-pct': 2654.0,
            '.threads.fullcnt': 1324492.0,
            '.threads.threads': 8.0,
            '.v2.unknown': 18.0,
            '.v3.access': 136921.0,
            '.v3.commit': 635.0,
            '.v3.create': 1655.0,
            '.v3.fsinfo': 11.0,
            '.v3.fsstat': 34450.0,
            '.v3.getattr': 724974.0,
            '.v3.lookup': 213165.0,
            '.v3.null': 8.0,
            '.v3.read': 8761683.0,
            '.v3.readdir': 11295.0,
            '.v3.readdirplus': 132298.0,
            '.v3.remove': 1488.0,
            '.v3.unknown': 22.0,
            '.v3.write': 67937.0,
            '.v4.compound': 4476320.0,
            '.v4.null': 18.0,
            '.v4.ops.access': 2083822.0,
            '.v4.ops.close': 34801.0,
            '.v4.ops.commit': 3955.0,
            '.v4.ops.getattr': 2302848.0,
            '.v4.ops.getfh': 51791.0,
            '.v4.ops.lookup': 68501.0,
            '.v4.ops.open': 34847.0,
            '.v4.ops.open_conf': 29002.0,
            '.v4.ops.putfh': 4435270.0,
            '.v4.ops.putrootfh': 6237.0,
            '.v4.ops.read': 8030.0,
            '.v4.ops.readdir': 272.0,
            '.v4.ops.remove': 7802.0,
            '.v4.ops.renew': 28594.0,
            '.v4.ops.restorefh': 34839.0,
            '.v4.ops.savefh': 34847.0,
            '.v4.ops.setattr': 7870.0,
            '.v4.ops.setcltid': 6226.0,
            '.v4.ops.setcltidconf': 6227.0,
            '.v4.ops.unknown': 40.0,
            '.v4.ops.write': 76562.0,
            '.v4.unknown': 2.0
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

################################################################################
if __name__ == "__main__":
    unittest.main()
