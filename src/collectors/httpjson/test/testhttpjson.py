#!/usr/bin/python
# coding=utf-8
##########################################################################
from test import CollectorTestCase
from test import get_collector_config
from mock import Mock
from mock import patch
from diamond.collector import Collector
from httpjson import HTTPJSONCollector

##########################################################################


class TestHTTPJSONCollector(CollectorTestCase):

    def setUp(self):
        config = get_collector_config('HTTPJSONCollector', {})
        self.collector = HTTPJSONCollector(config, None)

    def test_import(self):
        self.assertTrue(HTTPJSONCollector)

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        urlopen_mock = patch('urllib2.urlopen',
                             Mock(return_value=self.getFixture('stats.json')))

        urlopen_mock.start()
        self.collector.collect()
        urlopen_mock.stop()

        metrics = self.getPickledResults("real_stat.pkl")

        self.assertPublishedMany(publish_mock, metrics)
