#!/usr/bin/python
# coding=utf-8
###############################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import Mock
from mock import patch

from diamond.collector import Collector

from varnish import VarnishCollector

###############################################################################


class TestVarnishCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('VarnishCollector', {})

        self.collector = VarnishCollector(config, None)

    def test_import(self):
        self.assertTrue(VarnishCollector)

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        collector_mock = patch.object(VarnishCollector, 'poll', Mock(
                return_value=self.getFixture('varnish_stats').getvalue()))
        collector_mock.start()
        self.collector.collect()
        collector_mock.stop()

        metrics = {
            'client_conn': 10799,
            'client_drop': 0,
            'client_req': 10796,
            'cache_hit': 6580,
            'cache_hitpass': 0,
            'cache_miss': 2566,
            'backend_conn': 13363,
            'backend_unhealthy': 0,
            'backend_busy': 0,
            'backend_fail': 0,
            'backend_reuse': 0,
            'backend_toolate': 0,
            'backend_recycle': 0,
            'backend_retry': 0,
            'fetch_head': 0,
            'fetch_length': 12986,
            'fetch_chunked': 0,
            'fetch_eof': 0,
            'fetch_bad': 0,
            'fetch_close': 331,
            'fetch_oldhttp': 0,
            'fetch_zero': 0,
            'fetch_failed': 0,
            'n_sess_mem': 19,
            'n_sess': 1,
            'n_object': 9,
            'n_vampireobject': 0,
            'n_objectcore': 17,
            'n_objecthead': 27,
            'n_waitinglist': 10,
            'n_vbc': 1,
            'n_wrk': 10,
            'n_wrk_create': 10,
            'n_wrk_failed': 0,
            'n_wrk_max': 11451,
            'n_wrk_lqueue': 0,
            'n_wrk_queued': 0,
            'n_wrk_drop': 0,
            'n_backend': 4,
            'n_expired': 2557,
            'n_lru_nuked': 0,
            'n_lru_moved': 5588,
            'losthdr': 0,
            'n_objsendfile': 0,
            'n_objwrite': 2546,
            'n_objoverflow': 0,
            's_sess': 10798,
            's_req': 10796,
            's_pipe': 0,
            's_pass': 10796,
            's_fetch': 13362,
            's_hdrbytes': 4764593,
            's_bodybytes': 23756354,
            'sess_closed': 10798,
            'sess_pipeline': 0,
            'sess_readahead': 0,
            'sess_linger': 0,
            'sess_herd': 0,
            'shm_records': 1286246,
            'shm_writes': 102894,
            'shm_flushes': 0,
            'shm_cont': 0,
            'shm_cycles': 0,
            'sms_nreq': 0,
            'sms_nobj': 0,
            'sms_nbytes': 0,
            'sms_balloc': 0,
            'sms_bfree': 0,
            'backend_req': 13363,
            'n_vcl': 1,
            'n_vcl_avail': 1,
            'n_vcl_discard': 0,
            'n_ban': 1,
            'n_ban_add': 1,
            'n_ban_retire': 0,
            'n_ban_obj_test': 0,
            'n_ban_re_test': 0,
            'n_ban_dups': 0,
            'hcb_nolock': 9146,
            'hcb_lock': 2379,
            'hcb_insert': 2379,
            'accept_fail': 0,
            'client_drop_late': 0,
            'uptime': 35440,
            'dir_dns_lookups': 0,
            'dir_dns_failed': 0,
            'dir_dns_hit': 0,
            'dir_dns_cache_full': 0,
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

    @patch.object(Collector, 'publish')
    def test_should_fail_gracefully(self, publish_mock):
        collector_mock = patch.object(VarnishCollector, 'poll', Mock(
                return_value=self.getFixture(
                    'varnish_stats_blank').getvalue()))
        collector_mock.start()
        self.collector.collect()
        collector_mock.stop()

        self.assertPublishedMany(publish_mock, {})

###############################################################################
if __name__ == "__main__":
    unittest.main()
