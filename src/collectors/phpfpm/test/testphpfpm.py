#!/usr/bin/python
# coding=utf-8
##########################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import Mock
from mock import patch

from diamond.collector import Collector
from phpfpm import PhpFpmCollector

##########################################################################


class TestPhpFpmCollector(CollectorTestCase):

    def setUp(self):
        config = get_collector_config('PhpFpmCollector', {
            'interval': 10
        })

        self.collector = PhpFpmCollector(config, None)

    def test_import(self):
        self.assertTrue(PhpFpmCollector)

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        patch_urlopen = patch('urllib2.urlopen', Mock(
            return_value=self.getFixture('stats')))

        patch_urlopen.start()
        self.collector.collect()
        patch_urlopen.stop()

        metrics = {
            'accepted_conn': 777335,
            'listen_queue': 0,
            'max_listen_queue': 0,
            'listen_queue_len': 0,
            'idle_processes': 502,
            'active_processes': 14,
            'total_processes': 516,
            'max_active_processes': 515,
            'max_children_reached': 0,
            'slow_requests': 0,
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
