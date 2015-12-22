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

from os import path
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

        with open(path.join(path.dirname(__file__),
                            'metrics.json'), 'rb') as fp:
            metrics = json.load(fp)

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

###############################################################################
if __name__ == "__main__":
    unittest.main()
