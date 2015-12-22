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
from xfs import XFSCollector

################################################################################


class TestXFSCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('XFSCollector', {
            'interval': 1
        })

        self.collector = XFSCollector(config, None)

    def test_import(self):
        self.assertTrue(XFSCollector)

    @patch('__builtin__.open')
    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_open_proc_stat(self, publish_mock, open_mock):
        open_mock.return_value = StringIO('')
        self.collector.collect()
        open_mock.assert_called_once_with('/proc/fs/xfs/stat')

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        XFSCollector.PROC = self.getFixturePath('proc_fs_xfs_stat-1')
        self.collector.collect()

        self.assertPublishedMany(publish_mock, {})

        XFSCollector.PROC = self.getFixturePath('proc_fs_xfs_stat-2')
        self.collector.collect()

        metrics = {
            'extent_alloc.alloc_extent': 58,
            'extent_alloc.alloc_block': 928,
            'extent_alloc.free_extent': 116,
            'extent_alloc.free_block': 928,
            'abt.lookup': 0,
            'abt.compare': 0,
            'abt.insrec': 0,
            'abt.delrec': 0,
            'blk_map.read_ops': 124647,
            'blk_map.write_ops': 116,
            'blk_map.unmap': 116,
            'blk_map.add_exlist': 58,
            'blk_map.del_exlist': 116,
            'blk_map.look_exlist': 124879,
            'blk_map.cmp_exlist': 0,
            'bmbt.lookup': 0,
            'bmbt.compare': 0,
            'bmbt.insrec': 0,
            'bmbt.delrec': 0,
            'dir.lookup': 49652,
            'dir.create': 58,
            'dir.remove': 58,
            'dir.getdents': 334948,
            'trans.sync': 7,
            'trans.async': 586,
            'trans.empty': 0,
            'ig.ig_attempts': 0,
            'ig.ig_found': 13142,
            'ig.ig_frecycle': 0,
            'ig.ig_missed': 34759,
            'ig.ig_dup': 0,
            'ig.ig_reclaims': 110424,
            'ig.ig_attrchg': 0,
            'log.writes': 65,
            'log.blocks': 8320,
            'log.noiclogs': 0,
            'log.force': 681,
            'log.force_sleep': 65,
            'push_ail.try_logspace': 13403,
            'push_ail.sleep_logspace': 0,
            'push_ail.pushes': 2521,
            'push_ail.success': 41,
            'push_ail.pushbuf': 144,
            'push_ail.pinned': 0,
            'push_ail.locked': 0,
            'push_ail.flushing': 0,
            'push_ail.restarts': 0,
            'push_ail.flush': 0,
            'xstrat.quick': 58,
            'xstrat.split': 0,
            'rw.write_calls': 584,
            'rw.read_calls': 1909917,
            'attr.get': 54995,
            'attr.set': 0,
            'attr.remove': 0,
            'attr.list': 0,
            'icluster.iflush_count': 49,
            'icluster.icluster_flushcnt': 16,
            'icluster.icluster_flushinode': 16,
            'vnodes.vn_active': 0,
            'vnodes.vn_alloc': 0,
            'vnodes.vn_get': 0,
            'vnodes.vn_hold': 0,
            'vnodes.vn_rele': 110462,
            'vnodes.vn_reclaim': 110462,
            'vnodes.vn_remove': 110462,
            'vnodes.vn_free': 0,
            'buf.xb_get': 39013,
            'buf.xb_create': 6671,
            'buf.xb_get_locked': 32391,
            'buf.xb_get_locked_waited': 0,
            'buf.xb_busy_locked': 0,
            'buf.xb_miss_locked': 6671,
            'buf.xb_page_retries': 0,
            'buf.xb_page_found': 13217,
            'buf.xb_get_read': 6671,
            'abtb2.xs_abtb_2_lookup': 203,
            'abtb2.xs_abtb_2_compare': 1876,
            'abtb2.xs_abtb_2_insrec': 47,
            'abtb2.xs_abtb_2_delrec': 47,
            'abtb2.xs_abtb_2_newroot': 0,
            'abtb2.xs_abtb_2_killroot': 0,
            'abtb2.xs_abtb_2_increment': 0,
            'abtb2.xs_abtb_2_decrement': 0,
            'abtb2.xs_abtb_2_lshift': 0,
            'abtb2.xs_abtb_2_rshift': 0,
            'abtb2.xs_abtb_2_split': 0,
            'abtb2.xs_abtb_2_join': 0,
            'abtb2.xs_abtb_2_alloc': 0,
            'abtb2.xs_abtb_2_free': 0,
            'abtb2.xs_abtb_2_moves': 7040,
            'abtc2.xs_abtc_2_lookup': 422,
            'abtc2.xs_abtc_2_compare': 4014,
            'abtc2.xs_abtc_2_insrec': 203,
            'abtc2.xs_abtc_2_delrec': 203,
            'abtc2.xs_abtc_2_newroot': 0,
            'abtc2.xs_abtc_2_killroot': 0,
            'abtc2.xs_abtc_2_increment': 0,
            'abtc2.xs_abtc_2_decrement': 0,
            'abtc2.xs_abtc_2_lshift': 0,
            'abtc2.xs_abtc_2_rshift': 0,
            'abtc2.xs_abtc_2_split': 0,
            'abtc2.xs_abtc_2_join': 0,
            'abtc2.xs_abtc_2_alloc': 0,
            'abtc2.xs_abtc_2_free': 0,
            'abtc2.xs_abtc_2_moves': 34516,
            'bmbt2.xs_bmbt_2_lookup': 0,
            'bmbt2.xs_bmbt_2_compare': 0,
            'bmbt2.xs_bmbt_2_insrec': 0,
            'bmbt2.xs_bmbt_2_delrec': 0,
            'bmbt2.xs_bmbt_2_newroot': 0,
            'bmbt2.xs_bmbt_2_killroot': 0,
            'bmbt2.xs_bmbt_2_increment': 0,
            'bmbt2.xs_bmbt_2_decrement': 0,
            'bmbt2.xs_bmbt_2_lshift': 0,
            'bmbt2.xs_bmbt_2_rshift': 0,
            'bmbt2.xs_bmbt_2_split': 0,
            'bmbt2.xs_bmbt_2_join': 0,
            'bmbt2.xs_bmbt_2_alloc': 0,
            'bmbt2.xs_bmbt_2_free': 0,
            'bmbt2.xs_bmbt_2_moves': 0,
            'ibt2.lookup': 138,
            'ibt2.compare': 1214,
            'ibt2.insrec': 0,
            'ibt2.delrec': 0,
            'ibt2.newroot': 0,
            'ibt2.killroot': 0,
            'ibt2.increment': 0,
            'ibt2.decrement': 0,
            'ibt2.lshift': 0,
            'ibt2.rshift': 0,
            'ibt2.split': 0,
            'ibt2.join': 0,
            'ibt2.alloc': 0,
            'ibt2.free': 0,
            'ibt2.moves': 0,
            'xpc.xs_xstrat_bytes': 3801088,
            'xpc.xs_write_bytes': 270944,
            'xpc.xs_read_bytes': 2953097143,
            'debug.debug': 0
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

################################################################################
if __name__ == "__main__":
    unittest.main()
