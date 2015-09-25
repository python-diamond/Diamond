#!/usr/bin/python
# coding=utf-8
########################################################################

from test import CollectorTestCase
from test import get_collector_config
from mock import patch

from diamond.collector import Collector

from websitemonitor import WebsiteMonitorCollector

########################################################################


class MockResponse(object):

    def __init__(self, resp_data, code=200):
        self.resp_data = resp_data
        self.code = code

    def read(self):
        return self.resp_data

    def getcode(self):
        return self.code


class TestWebsiteCollector(CollectorTestCase):

    def setUp(self, config=None):
        if config is None:
            config = get_collector_config('WebsiteCollector', {
                'url': ''
            })
        else:
            config = get_collector_config('WebsiteCollector', config)

        self.collector = WebsiteMonitorCollector(config, None)

        self.patcher = patch('urllib2.urlopen')
        self.urlopen_mock = self.patcher.start()

    def test_import(self):
        self.assertTrue(WebsiteMonitorCollector)

    @patch.object(Collector, 'publish')
    def test_websitemonitorcollector_with_data(self, publish_mock):

        self.collector.collect()

        self.urlopen_mock.return_value = MockResponse(200)

        metrics = {}

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])

        self.assertPublishedMany([publish_mock], metrics)

    @patch.object(Collector, 'publish')
    def test_websitemonitorcollector(self, publish_mock):
        self.setUp()

        self.collector.collect()

        self.assertPublishedMany(publish_mock, {
        })

    def tearDown(self):
        self.patcher.stop()
