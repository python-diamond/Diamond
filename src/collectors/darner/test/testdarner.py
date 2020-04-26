#!/usr/bin/python
# coding=utf-8
###############################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import Mock
from mock import patch

from diamond.collector import Collector
from darner import DarnerCollector

###############################################################################


class TestDarnerCollector(CollectorTestCase):

    def setUp(self):
        config = get_collector_config('DarnerCollector', {
            'interval': 10,
            'hosts': ['localhost:22133'],
        })

        self.collector = DarnerCollector(config, None)

    def test_import(self):
        self.assertTrue(DarnerCollector)

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        patch_raw_stats1 = patch.object(
            DarnerCollector,
            'get_raw_stats',
            Mock(return_value=self.getFixture(
                'stats1').getvalue()))

        patch_raw_stats2 = patch.object(
            DarnerCollector,
            'get_raw_stats',
            Mock(return_value=self.getFixture(
                'stats2').getvalue()))

        patch_raw_stats1.start()
        self.collector.collect()
        patch_raw_stats1.stop()

        self.assertPublishedMany(publish_mock, {})

        patch_raw_stats2.start()
        self.collector.collect()
        patch_raw_stats2.stop()

        metrics = {
            'localhost.uptime': 2422175,
            'localhost.total_items': 20,
            'localhost.curr_connections': 2,
            'localhost.total_connections': 15,
            'localhost.cmd_get': 100,
            'localhost.cmd_set': 150,
            'localhost.queues.test1.items': 2,
            'localhost.queues.test1.waiters': 4,
            'localhost.queues.test1.open_transactions': 8,
            'localhost.queues.test_2.items': 16,
            'localhost.queues.test_2.waiters': 32,
            'localhost.queues.test_2.open_transactions': 64,
            'localhost.queues.test_3_bar.items': 128,
            'localhost.queues.test_3_bar.waiters': 256,
            'localhost.queues.test_3_bar.open_transactions': 512,
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

###############################################################################
if __name__ == "__main__":
    unittest.main()
