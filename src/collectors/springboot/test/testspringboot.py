#!/usr/bin/python
# coding=utf-8
################################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import Mock
from mock import patch

from diamond.collector import Collector

from springboot import SpringBootCollector

################################################################################


class TestSpringBootCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('SpringBootCollector', {})

        self.collector = SpringBootCollector(config, None)

    def test_import(self):
        self.assertTrue(SpringBootCollector)

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        patch_urlopen = patch('urllib2.urlopen',
                              Mock(return_value=self.getFixture('stats')))

        patch_urlopen.start()
        self.collector.collect()
        patch_urlopen.stop()

        metrics = {
            'gauge.performance.AuthenticationProvider.authenticate.min': 9.142272E7,
            'heap.used': 1.29674584E8,
            'heap.init': 1.13901568E9,
            'classes': 1000,
            'instance.uptime': 30,
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

################################################################################
if __name__ == "__main__":
    unittest.main()
