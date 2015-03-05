#!/usr/bin/python
# coding=utf-8
###############################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import Mock
from mock import patch

from diamond.collector import Collector
from twemproxy import TwemproxyCollector

try:
    import simplejson as json
except ImportError:
    import json

###############################################################################


class TestTwemproxyCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('TwemproxyCollector', {
            'interval': 60,
            'hosts': ['localhost:22222'],
        })

        self.collector = TwemproxyCollector(config, None)

    def test_import(self):
        self.assertTrue(TwemproxyCollector)

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        patch_raw_stats1 = patch.object(
            TwemproxyCollector,
            'get_raw_stats',
            Mock(return_value=json.loads(self.getFixture(
                'stats1').getvalue())))

        patch_raw_stats2 = patch.object(
            TwemproxyCollector,
            'get_raw_stats',
            Mock(return_value=json.loads(self.getFixture(
                'stats2').getvalue())))

        patch_raw_stats1.start()
        self.collector.collect()
        patch_raw_stats1.stop()

        self.assertPublishedMany(publish_mock, {})

        patch_raw_stats2.start()
        self.collector.collect()
        patch_raw_stats2.stop()

        metrics = {
            'localhost.uptime': 703137,
            'localhost.curr_connections': 5,
            'localhost.total_connections': 4.8499999999999996,
            'localhost.pools.development.client_connections': 358,
            'localhost.pools.development.client_eof': 2.0,
            'localhost.pools.development.client_err': 2.5166666666666666,
            'localhost.pools.development.forward_error': 0,
            'localhost.pools.development.fragments': 376.80000000000001,
            'localhost.pools.development.server_ejects': 0,
            'localhost.pools.development.servers.127_0_0_95.in_queue': 0,
            'localhost.pools.development.servers.127_0_0_95.in_queue_bytes': 0,
            'localhost.pools.development.servers.127_0_0_95.out_queue': 0,
            'localhost.pools.development.servers.127_0_0_95.out_queue_bytes': 0,
            'localhost.pools.development.servers.127_0_0_95.request_bytes': 817584.06666666665,
            'localhost.pools.development.servers.127_0_0_95.requests': 215.88333333333333,
            'localhost.pools.development.servers.127_0_0_95.response_bytes': 61628.683333333334,
            'localhost.pools.development.servers.127_0_0_95.responses': 215.75,
            'localhost.pools.development.servers.127_0_0_95.server_connections': 100,
            'localhost.pools.development.servers.127_0_0_95.server_eof': 0,
            'localhost.pools.development.servers.127_0_0_95.server_err': 0,
            'localhost.pools.development.servers.127_0_0_95.server_timedout': 0,
            'localhost.pools.development.servers.127_0_0_96.in_queue': 0,
            'localhost.pools.development.servers.127_0_0_96.in_queue_bytes': 0,
            'localhost.pools.development.servers.127_0_0_96.out_queue': 0,
            'localhost.pools.development.servers.127_0_0_96.out_queue_bytes': 0,
            'localhost.pools.development.servers.127_0_0_96.request_bytes': 357937.54999999999,
            'localhost.pools.development.servers.127_0_0_96.requests': 229.19999999999999,
            'localhost.pools.development.servers.127_0_0_96.response_bytes': 84637.366666666669,
            'localhost.pools.development.servers.127_0_0_96.responses': 229.16666666666666,
            'localhost.pools.development.servers.127_0_0_96.server_connections': 100,
            'localhost.pools.development.servers.127_0_0_96.server_eof': 1.6666666666666667,
            'localhost.pools.development.servers.127_0_0_96.server_err': 0,
            'localhost.pools.development.servers.127_0_0_96.server_timedout': 0,
            'localhost.pools.production.client_connections': 358,
            'localhost.pools.production.client_eof': 2.0,
            'localhost.pools.production.client_err': 2.5166666666666666,
            'localhost.pools.production.forward_error': 0,
            'localhost.pools.production.fragments': 376.80000000000001,
            'localhost.pools.production.server_ejects': 0,
            'localhost.pools.production.servers.127_0_0_92.in_queue': 0,
            'localhost.pools.production.servers.127_0_0_92.in_queue_bytes': 0,
            'localhost.pools.production.servers.127_0_0_92.out_queue': 0,
            'localhost.pools.production.servers.127_0_0_92.out_queue_bytes': 0,
            'localhost.pools.production.servers.127_0_0_92.request_bytes': 631888.91666666663,
            'localhost.pools.production.servers.127_0_0_92.requests': 229.34999999999999,
            'localhost.pools.production.servers.127_0_0_92.response_bytes': 56435.183333333334,
            'localhost.pools.production.servers.127_0_0_92.responses': 229.25,
            'localhost.pools.production.servers.127_0_0_92.server_connections': 100,
            'localhost.pools.production.servers.127_0_0_92.server_eof': 0,
            'localhost.pools.production.servers.127_0_0_92.server_err': 0,
            'localhost.pools.production.servers.127_0_0_92.server_timedout': 0,
            'localhost.pools.production.servers.127_0_0_93.in_queue': 1,
            'localhost.pools.production.servers.127_0_0_93.in_queue_bytes': 38,
            'localhost.pools.production.servers.127_0_0_93.out_queue': 0,
            'localhost.pools.production.servers.127_0_0_93.out_queue_bytes': 0,
            'localhost.pools.production.servers.127_0_0_93.request_bytes': 939547.33333333337,
            'localhost.pools.production.servers.127_0_0_93.requests': 280.43333333333334,
            'localhost.pools.production.servers.127_0_0_93.response_bytes': 246464.14999999999,
            'localhost.pools.production.servers.127_0_0_93.responses': 280.28333333333336,
            'localhost.pools.production.servers.127_0_0_93.server_connections': 100,
            'localhost.pools.production.servers.127_0_0_93.server_eof': 0,
            'localhost.pools.production.servers.127_0_0_93.server_err': 0,
            'localhost.pools.production.servers.127_0_0_93.server_timedout': 0.71666666666666667,
            'localhost.pools.production.servers.127_0_0_94.in_queue': 0,
            'localhost.pools.production.servers.127_0_0_94.in_queue_bytes': 0,
            'localhost.pools.production.servers.127_0_0_94.out_queue': 0,
            'localhost.pools.production.servers.127_0_0_94.out_queue_bytes': 0,
            'localhost.pools.production.servers.127_0_0_94.request_bytes': 413543.0,
            'localhost.pools.production.servers.127_0_0_94.requests': 247.09999999999999,
            'localhost.pools.production.servers.127_0_0_94.response_bytes': 361848.84999999998,
            'localhost.pools.production.servers.127_0_0_94.responses': 247.08333333333334,
            'localhost.pools.production.servers.127_0_0_94.server_connections': 100,
            'localhost.pools.production.servers.127_0_0_94.server_eof': 0,
            'localhost.pools.production.servers.127_0_0_94.server_err': 0,
            'localhost.pools.production.servers.127_0_0_94.server_timedout': 0
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

###############################################################################
if __name__ == "__main__":
    unittest.main()
