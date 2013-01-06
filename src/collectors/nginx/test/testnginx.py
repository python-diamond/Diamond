#!/usr/bin/python
# coding=utf-8
################################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import Mock
from mock import patch

from diamond.collector import Collector

from nginx import NginxCollector

################################################################################


class TestNginxCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('NginxCollector', {})

        self.collector = NginxCollector(config, None)

    def test_import(self):
        self.assertTrue(NginxCollector)

    @patch.object(Collector, 'publish')
    @patch.object(Collector, 'publish_gauge')
    @patch.object(Collector, 'publish_counter')
    def test_should_work_with_real_data(self, publish_counter_mock,
                                        publish_gauge_mock, publish_mock):
        patch_urlopen = patch('urllib2.urlopen', Mock(
            return_value=self.getFixture('status')))

        patch_urlopen.start()
        self.collector.collect()
        patch_urlopen.stop()

        metrics = {
            'active_connections': 3,
            'conn_accepted': 396396,
            'conn_handled': 396396,
            'req_handled': 396396,
            'act_reads': 2,
            'act_writes': 1,
            'act_waits': 0,
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany([publish_mock,
                                  publish_gauge_mock,
                                  publish_counter_mock
                                  ], metrics)

    @patch.object(Collector, 'publish')
    def test_should_fail_gracefully(self, publish_mock):
        patch_urlopen = patch('urllib2.urlopen', Mock(
            return_value=self.getFixture('status_blank')))

        patch_urlopen.start()
        self.collector.collect()
        patch_urlopen.stop()

        self.assertPublishedMany(publish_mock, {})

################################################################################
if __name__ == "__main__":
    unittest.main()
