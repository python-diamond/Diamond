#!/usr/bin/python
# coding=utf-8
################################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import Mock
from mock import patch

from diamond.collector import Collector
from haproxy import HAProxyCollector

################################################################################


class TestHAProxyCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('HAProxyCollector', {
            'interval': 10,
        })

        self.collector = HAProxyCollector(config, None)

    def test_import(self):
        self.assertTrue(HAProxyCollector)

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        self.collector.config['ignore_servers'] = False

        patch_urlopen = patch('urllib2.urlopen',
                              Mock(return_value=self.getFixture('stats.csv')))

        patch_urlopen.start()
        self.collector.collect()
        patch_urlopen.stop()

        metrics = self.getPickledResults('real_data.pkl')

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data_and_ignore_servers(self, publish_mock):
        self.collector.config['ignore_servers'] = True

        patch_urlopen = patch('urllib2.urlopen',
                              Mock(return_value=self.getFixture('stats.csv')))

        patch_urlopen.start()
        self.collector.collect()
        patch_urlopen.stop()

        metrics = self.getPickledResults('real_data_ignore_servers.pkl')

        self.assertPublishedMany(publish_mock, metrics)

################################################################################
if __name__ == "__main__":
    unittest.main()
