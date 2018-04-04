#!/usr/bin/python
# coding=utf-8
##########################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import Mock
from mock import patch

from diamond.collector import Collector

from dropwizard import DropwizardCollector

##########################################################################


class TestDropwizardCollector(CollectorTestCase):

    def setUp(self):
        config = get_collector_config('DropwizardCollector', {})

        self.collector = DropwizardCollector(config, None)

    def test_import(self):
        self.assertTrue(DropwizardCollector)

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        patch_urlopen = patch('urllib2.urlopen',
                              Mock(return_value=self.getFixture('stats')))

        patch_urlopen.start()
        self.collector.collect()
        patch_urlopen.stop()

        metrics = {
            'io.dropwizard.post-requests.count': 22289,
            'io.dropwizard.post-requests.max': 3.232,
            'io.dropwizard.post-requests.min': 0.3194237337346423,
            'io.dropwizard.post-requests.mean': 0.008,
            'io.dropwizard.post-requests.p50': 0.036000000000000004,
            'io.dropwizard.post-requests.p75': 1.024,
            'io.dropwizard.post-requests.p95': 1.054,
            'io.dropwizard.post-requests.p98': 1.088,
            'io.dropwizard.post-requests.p99': 1.213,
            'io.dropwizard.post-requests.p999': 1.213,
            'io.dropwizard.post-requests.stddev': 0.4589858539681931,
            'io.dropwizard.post-requests.m15_rate': 0.4634860629747088,
            'io.dropwizard.post-requests.m1_rate': 0.9938835145446502,
            'io.dropwizard.post-requests.m5_rate': 0.5811914520408888,
            'io.dropwizard.post-requests.mean_rate': 0.27133960525475337,
            'test.count': 3,
            'test.max': 4,
            'test.min': 2,
            'test.mean': 3,
            'test.p50': 3,
            'test.p75': 4,
            'test.p95': 4,
            'test.p98': 4,
            'test.p99': 4,
            'test.p999': 4,
            'test.stddev': 0.816496580927726,
            'io.dropwizard.active-requests.count': 0,
            'io.dropwizard.active-suspended.count': 0,
            'io.dropwizard.percent-4xx-15m': 0,
            'jvm.attribute.uptime': 82163833,
            'io.dropwizard.1xx-responses.count': 0,
            'io.dropwizard.1xx-responses.m15_rate': 0,
            'io.dropwizard.1xx-responses.m1_rate': 0,
            'io.dropwizard.1xx-responses.m5_rate': 0,
            'io.dropwizard.1xx-responses.mean_rate': 0
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

    @patch.object(Collector, 'publish')
    def test_should_fail_gracefully(self, publish_mock):
        patch_urlopen = patch(
            'urllib2.urlopen',
            Mock(
                return_value=self.getFixture('stats_blank')))

        patch_urlopen.start()
        self.collector.collect()
        patch_urlopen.stop()

        self.assertPublishedMany(publish_mock, {})

##########################################################################
if __name__ == "__main__":
    unittest.main()
