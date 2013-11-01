#!/usr/bin/python
# coding=utf-8
################################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import Mock
from mock import patch

from diamond.collector import Collector
from httpd import HttpdCollector
import httplib

################################################################################


class TestHTTPResponse(httplib.HTTPResponse):
    def __init__(self):
        pass

    def read(self):
        pass


class TestHttpdCollector(CollectorTestCase):
    def setUp(self, config=None):
        if config is None:
            config = get_collector_config('HttpdCollector', {
                'interval': '10',
                'url':      ''
            })
        else:
            config = get_collector_config('HttpdCollector', config)

        self.collector = HttpdCollector(config, None)

        self.HTTPResponse = TestHTTPResponse()

        httplib.HTTPConnection.request = Mock(return_value=True)
        httplib.HTTPConnection.getresponse = Mock(
            return_value=self.HTTPResponse)

    def test_import(self):
        self.assertTrue(HttpdCollector)

    @patch.object(Collector, 'publish')
    def test_should_work_with_synthetic_data(self, publish_mock):
        self.setUp()

        patch_read = patch.object(TestHTTPResponse,
                                  'read',
                                  Mock(return_value=self.getFixture(
                                    'server-status-fake-1').getvalue()))

        patch_headers = patch.object(TestHTTPResponse,
                                     'getheaders',
                                     Mock(return_value={}))

        patch_headers.start()
        patch_read.start()
        self.collector.collect()
        patch_read.stop()

        self.assertPublishedMany(publish_mock, {})

        patch_read = patch.object(TestHTTPResponse,
                                  'read',
                                  Mock(return_value=self.getFixture(
                                    'server-status-fake-2').getvalue()))

        patch_read.start()
        self.collector.collect()
        patch_read.stop()
        patch_headers.stop()

        self.assertPublishedMany(publish_mock, {
            'TotalAccesses': 100,
            'ReqPerSec': 10,
            'BytesPerSec': 20480,
            'BytesPerReq': 204,
            'BusyWorkers': 6,
            'IdleWorkers': 4,
        })

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        self.setUp()

        patch_read = patch.object(TestHTTPResponse,
                                  'read',
                                  Mock(return_value=self.getFixture(
                                    'server-status-live-1').getvalue()))

        patch_headers = patch.object(TestHTTPResponse,
                                     'getheaders',
                                     Mock(return_value={}))

        patch_headers.start()
        patch_read.start()
        self.collector.collect()
        patch_read.stop()

        self.assertPublishedMany(publish_mock, {})

        patch_read = patch.object(TestHTTPResponse,
                                  'read',
                                  Mock(return_value=self.getFixture(
                                    'server-status-live-2').getvalue()))

        patch_read.start()
        self.collector.collect()
        patch_read.stop()
        patch_headers.stop()

        metrics = {
            'TotalAccesses': 8314,
            'ReqPerSec': 0,
            'BytesPerSec': 165,
            'BytesPerReq': 5418,
            'BusyWorkers': 9,
            'IdleWorkers': 0,
        }
        self.assertPublishedMany(publish_mock, metrics)

    @patch.object(Collector, 'publish')
    def test_should_work_with_multiple_servers(self, publish_mock):
        self.setUp(config={
            'urls': [
                'nickname1 http://localhost:8080/server-status?auto',
                'nickname2 http://localhost:8080/server-status?auto',
            ],
        })

        patch_read = patch.object(TestHTTPResponse,
                                  'read',
                                  Mock(return_value=self.getFixture(
                                    'server-status-live-1').getvalue()))

        patch_headers = patch.object(TestHTTPResponse,
                                     'getheaders',
                                     Mock(return_value={}))

        patch_headers.start()
        patch_read.start()
        self.collector.collect()
        patch_read.stop()

        self.assertPublishedMany(publish_mock, {})

        patch_read = patch.object(TestHTTPResponse,
                                  'read',
                                  Mock(return_value=self.getFixture(
                                    'server-status-live-2').getvalue()))

        patch_read.start()
        self.collector.collect()
        patch_read.stop()
        patch_headers.stop()

        metrics = {
            'nickname1.TotalAccesses': 8314,
            'nickname1.ReqPerSec': 0,
            'nickname1.BytesPerSec': 165,
            'nickname1.BytesPerReq': 5418,
            'nickname1.BusyWorkers': 9,
            'nickname1.IdleWorkers': 0,

            'nickname2.TotalAccesses': 8314,
            'nickname2.ReqPerSec': 0,
            'nickname2.BytesPerSec': 165,
            'nickname2.BytesPerReq': 5418,
            'nickname2.BusyWorkers': 9,
            'nickname2.IdleWorkers': 0,
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

    @patch.object(Collector, 'publish')
    def test_issue_456(self, publish_mock):
        self.setUp(config={
            'urls': 'vhost http://localhost/server-status?auto',
        })

        patch_read = patch.object(TestHTTPResponse,
                                  'read',
                                  Mock(return_value=self.getFixture(
                                    'server-status-live-3').getvalue()))

        patch_headers = patch.object(TestHTTPResponse,
                                     'getheaders',
                                     Mock(return_value={}))

        patch_headers.start()
        patch_read.start()
        self.collector.collect()
        patch_read.stop()

        self.assertPublishedMany(publish_mock, {})

        patch_read = patch.object(TestHTTPResponse,
                                  'read',
                                  Mock(return_value=self.getFixture(
                                    'server-status-live-4').getvalue()))

        patch_read.start()
        self.collector.collect()
        patch_read.stop()
        patch_headers.stop()

        metrics = {
            'TotalAccesses': 329,
            'ReqPerSec': 0.156966,
            'BytesPerSec': 2417,
            'BytesPerReq': 15403,
            'BusyWorkers': 1,
            'IdleWorkers': 17,
        }
        self.assertPublishedMany(publish_mock, metrics)

################################################################################
if __name__ == "__main__":
    unittest.main()
