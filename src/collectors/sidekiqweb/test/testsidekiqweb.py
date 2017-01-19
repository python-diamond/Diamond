#!/usr/bin/python
# coding=utf-8
##########################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import Mock
from mock import patch

from diamond.collector import Collector
from sidekiqweb import SidekiqWebCollector

##########################################################################


class TestSidekiqWebCollector(CollectorTestCase):

    def setUp(self):
        config = get_collector_config('SidekiqWebCollector', {
            'interval': 10
        })

        self.collector = SidekiqWebCollector(config, None)

    def test_import(self):
        self.assertTrue(SidekiqWebCollector)

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        patch_urlopen = patch('urllib2.urlopen', Mock(
            return_value=self.getFixture('stats')))

        patch_urlopen.start()
        self.collector.collect()
        patch_urlopen.stop()

        metrics = {
            'redis.connected_clients': 22,
            'redis.uptime_in_days': 62,
            'redis.used_memory_human_byte': 1426063.36,
            'redis.used_memory_peak_human_byte': 8598323.2,
            'sidekiq.busy': 0,
            'sidekiq.default_latency': 0,
            'sidekiq.enqueued': 0,
            'sidekiq.failed': 22,
            'sidekiq.processed': 4622701,
            'sidekiq.retries': 0,
            'sidekiq.scheduled': 30,
        }

        self.assertPublishedMany(publish_mock, metrics)

    @patch.object(Collector, 'publish')
    def test_should_fail_gracefully(self, publish_mock):
        patch_urlopen = patch('urllib2.urlopen', Mock(
            return_value=self.getFixture('stats_blank')))

        patch_urlopen.start()
        self.collector.collect()
        patch_urlopen.stop()

        self.assertPublishedMany(publish_mock, {})

##########################################################################
if __name__ == "__main__":
    unittest.main()
