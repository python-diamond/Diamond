#!/usr/bin/python
# coding=utf-8
########################################################################
import httplib

from test import CollectorTestCase
from test import get_collector_config
from mock import Mock, patch

from diamond.collector import Collector

from websitemonitor import WebsiteMonitorCollector

########################################################################


class TestHTTPResponse(httplib.HTTPResponse):
    def __init__(self):
        pass

    def read(self):
        pass


class TestWebsiteCollector(CollectorTestCase):
    def setUp(self, config=None):
        if config is None:
            config = get_collector_config('WebsiteCollector', {
            'url': ''
        })
        else:
            config = get_collector_config('WebsiteCollector', config)

        self.collector = WebsiteMonitorCollector(config, None)

        self.HTTPResponse = TestHTTPResponse()

        httplib.HTTPConnection.request = Mock(return_value=True)
        httplib.HTTPConnection.getresponse = Mock(
            return_value=self.HTTPResponse)

    def test_import(self):
        self.assertTrue(WebsiteMonitorCollector)


    @patch.object(Collector, 'publish_counter')
    def test_websitemonitorcollector_with_data(self, publish_counter_mock):

        patch_read = patch.object(TestHTTPResponse, 'read',
                              Mock(return_value={'code': '200'}))

        patch_read.start()
        self.collector.collect()
        patch_read.stop()

        metrics = {
            'resp.code': 200,
            'rt': 8000
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                       metrics=metrics,
                       defaultpath=self.collector.config['path'])

        self.assertPublishedMany([publish_counter_mock], metrics)

    @patch.object(Collector, 'publish')
    def test_websitemonitorcollector(self, publish_mock):
        self.setUp()

        patch_read = patch.object(TestHTTPResponse, 'read', Mock(return_value={}))

        patch_read.start()
        self.collector.collect()
        patch_read.stop()

        self.assertPublishedMany(publish_mock, {
        })

