#!/usr/bin/python
# coding=utf-8
################################################################################
from StringIO import StringIO
from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import Mock
from mock import patch
import pickle
from diamond.collector import Collector
from jsoncommon import JSONCommonCollector

################################################################################


class TestJSONCommonCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('JSONCommonCollector', {})
        self.collector = JSONCommonCollector(config, None)

    def test_import(self):
        self.assertTrue(JSONCommonCollector)

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        urlopen_mock = patch('urllib2.urlopen', Mock(return_value=self.getFixture('stats.json')))

        urlopen_mock.start()
        self.collector.collect()
        urlopen_mock.stop()

        metrics = self.getPickledResults("real_stat.pkl")

        self.assertPublishedMany(publish_mock, metrics)
