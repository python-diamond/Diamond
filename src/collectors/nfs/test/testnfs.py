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
from nfs import NfsCollector

################################################################################


class TestNfsCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('NfsCollector', {
            'interval': 1
        })

        self.collector = NfsCollector(config, None)

    def test_import(self):
        self.assertTrue(NfsCollector)

    @patch('__builtin__.open')
    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_open_proc_stat(self, publish_mock, open_mock):
        open_mock.return_value = StringIO('')
        self.collector.collect()
        open_mock.assert_called_once_with('/proc/net/rpc/nfs')

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data_rhel5(self, publish_mock):
        NfsCollector.PROC = self.getFixturePath('rhel5-1')
        self.collector.collect()
        self.assertPublishedMany(publish_mock, {})

        NfsCollector.PROC = self.getFixturePath('rhel5-2')
        self.collector.collect()

        metrics = {
            'net.packets': 0.0,
            'net.tcpcnt': 0.0,
            'net.tcpconn': 0.0,
            'net.udpcnt': 0.0,
            'rpc.authrefrsh': 0.0,
            'rpc.calls': 8042864.0,
            'rpc.retrans': 0.0,
            'v2.create': 0.0,
            'v2.fsstat': 0.0,
            'v2.getattr': 0.0,
            'v2.link': 0.0,
            'v2.lookup': 0.0,
            'v2.mkdir': 0.0,
            'v2.null': 0.0,
            'v2.read': 0.0,
            'v2.readdir': 0.0,
            'v2.readlink': 0.0,
            'v2.remove': 0.0,
            'v2.rename': 0.0,
            'v2.rmdir': 0.0,
            'v2.root': 0.0,
            'v2.setattr': 0.0,
            'v2.symlink': 0.0,
            'v2.wrcache': 0.0,
            'v2.write': 0.0,
            'v3.access': 40672.0,
            'v3.commit': 0.0,
            'v3.create': 91.0,
            'v3.fsinfo': 0.0,
            'v3.fsstat': 20830.0,
            'v3.getattr': 162507.0,
            'v3.link': 0.0,
            'v3.lookup': 89.0,
            'v3.mkdir': 0.0,
            'v3.mknod': 0.0,
            'v3.null': 0.0,
            'v3.pathconf': 0.0,
            'v3.read': 6093419.0,
            'v3.readdir': 4002.0,
            'v3.readdirplus': 0.0,
            'v3.readlink': 0.0,
            'v3.remove': 9.0,
            'v3.rename': 0.0,
            'v3.rmdir': 0.0,
            'v3.setattr': 8640.0,
            'v3.symlink': 0.0,
            'v3.write': 1712605.0,
            'v4.access': 0.0,
            'v4.close': 0.0,
            'v4.commit': 0.0,
            'v4.confirm': 0.0,
            'v4.create': 0.0,
            'v4.delegreturn': 0.0,
            'v4.fs_locations': 0.0,
            'v4.fsinfo': 0.0,
            'v4.getacl': 0.0,
            'v4.getattr': 0.0,
            'v4.link': 0.0,
            'v4.lock': 0.0,
            'v4.lockt': 0.0,
            'v4.locku': 0.0,
            'v4.lookup': 0.0,
            'v4.lookup_root': 0.0,
            'v4.null': 0.0,
            'v4.open': 0.0,
            'v4.open_conf': 0.0,
            'v4.open_dgrd': 0.0,
            'v4.open_noat': 0.0,
            'v4.pathconf': 0.0,
            'v4.read': 0.0,
            'v4.readdir': 0.0,
            'v4.readlink': 0.0,
            'v4.rel_lkowner': 0.0,
            'v4.remove': 0.0,
            'v4.rename': 0.0,
            'v4.renew': 0.0,
            'v4.server_caps': 0.0,
            'v4.setacl': 0.0,
            'v4.setattr': 0.0,
            'v4.setclntid': 0.0,
            'v4.statfs': 0.0,
            'v4.symlink': 0.0,
            'v4.write': 0.0
        }

        self.assertPublishedMany(publish_mock, metrics)

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data_rhel6(self, publish_mock):
        NfsCollector.PROC = self.getFixturePath('rhel6-1')
        self.collector.collect()
        self.assertPublishedMany(publish_mock, {})

        NfsCollector.PROC = self.getFixturePath('rhel6-2')
        self.collector.collect()

        metrics = {
            'net.packets': 0.0,
            'net.tcpcnt': 0.0,
            'net.tcpconn': 0.0,
            'net.udpcnt': 0.0,
            'rpc.authrefrsh': 32.0,
            'rpc.calls': 32.0,
            'rpc.retrans': 0.0,
            'v2.create': 0.0,
            'v2.fsstat': 0.0,
            'v2.getattr': 0.0,
            'v2.link': 0.0,
            'v2.lookup': 0.0,
            'v2.mkdir': 0.0,
            'v2.null': 0.0,
            'v2.read': 0.0,
            'v2.readdir': 0.0,
            'v2.readlink': 0.0,
            'v2.remove': 0.0,
            'v2.rename': 0.0,
            'v2.rmdir': 0.0,
            'v2.root': 0.0,
            'v2.setattr': 0.0,
            'v2.symlink': 0.0,
            'v2.wrcache': 0.0,
            'v2.write': 0.0,
            'v3.access': 6.0,
            'v3.commit': 0.0,
            'v3.create': 0.0,
            'v3.fsinfo': 0.0,
            'v3.fsstat': 17.0,
            'v3.getattr': 7.0,
            'v3.link': 0.0,
            'v3.lookup': 0.0,
            'v3.mkdir': 0.0,
            'v3.mknod': 0.0,
            'v3.null': 0.0,
            'v3.pathconf': 0.0,
            'v3.read': 0.0,
            'v3.readdir': 0.0,
            'v3.readdirplus': 0.0,
            'v3.readlink': 0.0,
            'v3.remove': 0.0,
            'v3.rename': 0.0,
            'v3.rmdir': 0.0,
            'v3.setattr': 1.0,
            'v3.symlink': 0.0,
            'v3.write': 1.0,
            'v4.access': 0.0,
            'v4.close': 0.0,
            'v4.commit': 0.0,
            'v4.confirm': 0.0,
            'v4.create': 0.0,
            'v4.create_ses': 0.0,
            'v4.delegreturn': 0.0,
            'v4.destroy_ses': 0.0,
            'v4.ds_write': 0.0,
            'v4.exchange_id': 0.0,
            'v4.fs_locations': 0.0,
            'v4.fsinfo': 0.0,
            'v4.get_lease_t': 0.0,
            'v4.getacl': 0.0,
            'v4.getattr': 0.0,
            'v4.getdevinfo': 0.0,
            'v4.getdevlist': 0.0,
            'v4.layoutcommit': 0.0,
            'v4.layoutget': 0.0,
            'v4.layoutreturn': 0.0,
            'v4.link': 0.0,
            'v4.lock': 0.0,
            'v4.lockt': 0.0,
            'v4.locku': 0.0,
            'v4.lookup': 0.0,
            'v4.lookup_root': 0.0,
            'v4.null': 0.0,
            'v4.open': 0.0,
            'v4.open_conf': 0.0,
            'v4.open_dgrd': 0.0,
            'v4.open_noat': 0.0,
            'v4.pathconf': 0.0,
            'v4.read': 0.0,
            'v4.readdir': 0.0,
            'v4.readlink': 0.0,
            'v4.reclaim_comp': 0.0,
            'v4.rel_lkowner': 0.0,
            'v4.remove': 0.0,
            'v4.rename': 0.0,
            'v4.renew': 0.0,
            'v4.sequence': 0.0,
            'v4.server_caps': 0.0,
            'v4.setacl': 0.0,
            'v4.setattr': 0.0,
            'v4.setclntid': 0.0,
            'v4.statfs': 0.0,
            'v4.symlink': 0.0,
            'v4.write': 0.0,
        }

        self.assertPublishedMany(publish_mock, metrics)

################################################################################
if __name__ == "__main__":
    unittest.main()
