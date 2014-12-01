#!/usr/bin/python
# coding=utf-8
################################################################################

from test import CollectorTestCase
from test import get_collector_config
from mock import Mock
from mock import patch

from diamond.collector import Collector

from dseopscenter import DseOpsCenterCollector

################################################################################


class TestDseOpsCenterCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('DseOpsCenterCollector',
                                      {'cluster_id': 'MyTestCluster'})

        self.collector = DseOpsCenterCollector(config, None)

    def test_import(self):
        self.assertTrue(DseOpsCenterCollector)

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        urlopen_mock1 = patch('urllib2.urlopen', Mock(
            side_effect=lambda *args: self.getFixture('keyspaces.json')))
        urlopen_mock1.start()
        self.collector._get_schema()
        urlopen_mock1.stop()
        urlopen_mock2 = patch('urllib2.urlopen', Mock(
            side_effect=lambda *args: self.getFixture('new-metrics.json')))
        urlopen_mock2.start()
        self.collector.collect()
        urlopen_mock2.stop()

        metrics = {
            'cf-bf-false-positives.dse_system.leases': 0,
            'key-cache-requests': 38.28847822050253,
            'key-cache-hits': 9.114316945274672,
            'nonheap-max': 136314880,
            'nonheap-used': 48491696.666666664,
            'read-ops': 55.91526222229004,
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)
