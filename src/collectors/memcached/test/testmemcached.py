#!/usr/bin/python
# coding=utf-8
################################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import Mock
from mock import patch

from diamond.collector import Collector
from memcached import MemcachedCollector

################################################################################


class TestMemcachedCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('MemcachedCollector', {
            'interval': 10,
            'hosts': ['localhost:11211'],
        })

        self.collector = MemcachedCollector(config, None)

    def test_import(self):
        self.assertTrue(MemcachedCollector)

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        patch_raw_stats = patch.object(MemcachedCollector,
                                       'get_raw_stats',
                                       Mock(return_value=self.getFixture(
                                        'stats').getvalue()))

        patch_raw_stats.start()
        self.collector.collect()
        patch_raw_stats.stop()

        metrics = {
            'localhost.reclaimed': 0.000000,
            'localhost.expired_unfetched': 0.000000,
            'localhost.hash_is_expanding': 0.000000,
            'localhost.cas_hits': 0.000000,
            'localhost.uptime': 0,
            'localhost.touch_hits': 0.000000,
            'localhost.delete_misses': 0.000000,
            'localhost.listen_disabled_num': 0.000000,
            'localhost.cas_misses': 0.000000,
            'localhost.decr_hits': 0.000000,
            'localhost.cmd_touch': 0.000000,
            'localhost.incr_hits': 0.000000,
            'localhost.auth_cmds': 0.000000,
            'localhost.limit_maxbytes': 67108864.000000,
            'localhost.bytes_written': 0.000000,
            'localhost.incr_misses': 0.000000,
            'localhost.rusage_system': 0.195071,
            'localhost.total_items': 0.000000,
            'localhost.cmd_get': 0.000000,
            'localhost.curr_connections': 10.000000,
            'localhost.touch_misses': 0.000000,
            'localhost.threads': 4.000000,
            'localhost.total_connections': 0,
            'localhost.cmd_set': 0.000000,
            'localhost.curr_items': 0.000000,
            'localhost.conn_yields': 0.000000,
            'localhost.get_misses': 0.000000,
            'localhost.reserved_fds': 20.000000,
            'localhost.bytes_read': 0,
            'localhost.hash_bytes': 524288.000000,
            'localhost.evicted_unfetched': 0.000000,
            'localhost.cas_badval': 0.000000,
            'localhost.cmd_flush': 0.000000,
            'localhost.evictions': 0.000000,
            'localhost.bytes': 0.000000,
            'localhost.connection_structures': 11.000000,
            'localhost.hash_power_level': 16.000000,
            'localhost.auth_errors': 0.000000,
            'localhost.rusage_user': 0.231516,
            'localhost.delete_hits': 0.000000,
            'localhost.decr_misses': 0.000000,
            'localhost.get_hits': 0.000000,
            'localhost.repcached_qi_free': 0.000000,
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

################################################################################
if __name__ == "__main__":
    unittest.main()
