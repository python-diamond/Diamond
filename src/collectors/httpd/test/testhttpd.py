#!/usr/bin/python
# coding=utf-8
##########################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import Mock
from mock import patch

from diamond.collector import Collector
from httpd import HttpdCollector
import httplib

##########################################################################


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
                'url':      'http://www.example.com:80/server-status?auto'
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

        patch_read = patch.object(
            TestHTTPResponse,
            'read',
            Mock(return_value=self.getFixture(
                'server-status-fake-1').getvalue()))

        patch_headers = patch.object(
            TestHTTPResponse,
            'getheaders',
            Mock(return_value={}))

        patch_headers.start()
        patch_read.start()
        self.collector.collect()
        patch_read.stop()

        self.assertPublishedMany(publish_mock, {})

        patch_read = patch.object(
            TestHTTPResponse,
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
            'BytesPerReq': 204.8,
            'BusyWorkers': 6,
            'IdleWorkers': 4,
            'WritingWorkers': 1,
            'KeepaliveWorkers': 2,
            'ReadingWorkers': 3,
            'DnsWorkers': 0,
            'ClosingWorkers': 0,
            'LoggingWorkers': 0,
            'FinishingWorkers': 0,
            'CleanupWorkers': 0,
        })

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        self.setUp()

        patch_read = patch.object(
            TestHTTPResponse,
            'read',
            Mock(return_value=self.getFixture(
                'server-status-live-1').getvalue()))

        patch_headers = patch.object(
            TestHTTPResponse,
            'getheaders',
            Mock(return_value={}))

        patch_headers.start()
        patch_read.start()
        self.collector.collect()
        patch_read.stop()

        self.assertPublishedMany(publish_mock, {})

        patch_read = patch.object(
            TestHTTPResponse,
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
            'BytesPerReq': 5418.55,
            'BusyWorkers': 9,
            'IdleWorkers': 0,
            'WritingWorkers': 1,
            'KeepaliveWorkers': 7,
            'ReadingWorkers': 1,
            'DnsWorkers': 0,
            'ClosingWorkers': 0,
            'LoggingWorkers': 0,
            'FinishingWorkers': 0,
            'CleanupWorkers': 0,
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

        patch_read = patch.object(
            TestHTTPResponse,
            'read',
            Mock(return_value=self.getFixture(
                'server-status-live-1').getvalue()))

        patch_headers = patch.object(
            TestHTTPResponse,
            'getheaders',
            Mock(return_value={}))

        patch_headers.start()
        patch_read.start()
        self.collector.collect()
        patch_read.stop()

        self.assertPublishedMany(publish_mock, {})

        patch_read = patch.object(
            TestHTTPResponse,
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
            'nickname1.BytesPerReq': 5418.55,
            'nickname1.BusyWorkers': 9,
            'nickname1.IdleWorkers': 0,
            'nickname1.WritingWorkers': 1,
            'nickname1.KeepaliveWorkers': 7,
            'nickname1.ReadingWorkers': 1,
            'nickname1.DnsWorkers': 0,
            'nickname1.ClosingWorkers': 0,
            'nickname1.LoggingWorkers': 0,
            'nickname1.FinishingWorkers': 0,
            'nickname1.CleanupWorkers': 0,

            'nickname2.TotalAccesses': 8314,
            'nickname2.ReqPerSec': 0,
            'nickname2.BytesPerSec': 165,
            'nickname2.BytesPerReq': 5418.55,
            'nickname2.BusyWorkers': 9,
            'nickname2.IdleWorkers': 0,
            'nickname2.WritingWorkers': 1,
            'nickname2.KeepaliveWorkers': 7,
            'nickname2.ReadingWorkers': 1,
            'nickname2.DnsWorkers': 0,
            'nickname2.ClosingWorkers': 0,
            'nickname2.LoggingWorkers': 0,
            'nickname2.FinishingWorkers': 0,
            'nickname2.CleanupWorkers': 0,
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

        patch_read = patch.object(
            TestHTTPResponse,
            'read',
            Mock(return_value=self.getFixture(
                'server-status-live-3').getvalue()))

        patch_headers = patch.object(
            TestHTTPResponse,
            'getheaders',
            Mock(return_value={}))

        patch_headers.start()
        patch_read.start()
        self.collector.collect()
        patch_read.stop()

        self.assertPublishedMany(publish_mock, {})

        patch_read = patch.object(
            TestHTTPResponse,
            'read',
            Mock(return_value=self.getFixture(
                'server-status-live-4').getvalue()))

        patch_read.start()
        self.collector.collect()
        patch_read.stop()
        patch_headers.stop()

        metrics = {
            'vhost.TotalAccesses': 329,
            'vhost.ReqPerSec': 0.156966,
            'vhost.BytesPerSec': 2417.83,
            'vhost.BytesPerReq': 15403.6,
            'vhost.BusyWorkers': 1,
            'vhost.IdleWorkers': 17,
            'vhost.WritingWorkers': 1,
            'vhost.KeepaliveWorkers': 0,
            'vhost.ReadingWorkers': 0,
            'vhost.DnsWorkers': 0,
            'vhost.ClosingWorkers': 0,
            'vhost.LoggingWorkers': 0,
            'vhost.FinishingWorkers': 0,
            'vhost.CleanupWorkers': 0,
        }
        self.assertPublishedMany(publish_mock, metrics)

    @patch.object(Collector, 'publish')
    def test_issue_533(self, publish_mock):
        self.setUp(config={
            'urls': 'localhost http://localhost:80/server-status?auto,',
        })

        expected_urls = {'localhost': 'http://localhost:80/server-status?auto'}

        self.assertEqual(self.collector.urls, expected_urls)

    @patch.object(Collector, 'publish')
    def test_url_with_port(self, publish_mock):
        self.setUp(config={
            'urls': 'localhost http://localhost:80/server-status?auto',
        })

        expected_urls = {'localhost': 'http://localhost:80/server-status?auto'}

        self.assertEqual(self.collector.urls, expected_urls)

    @patch.object(Collector, 'publish')
    def test_url_without_port(self, publish_mock):
        self.setUp(config={
            'urls': 'localhost http://localhost/server-status?auto',
        })

        expected_urls = {'localhost': 'http://localhost/server-status?auto'}

        self.assertEqual(self.collector.urls, expected_urls)

    @patch.object(Collector, 'publish')
    def test_url_without_nickname(self, publish_mock):
        self.setUp(config={
            'urls': 'http://localhost/server-status?auto',
        })

        expected_urls = {'': 'http://localhost/server-status?auto'}

        self.assertEqual(self.collector.urls, expected_urls)

    @patch.object(Collector, 'publish')
    def test_issue_538(self, publish_mock):
        self.setUp(config={
            'enabled': True,
            'path_suffix': "",
            'ttl_multiplier': 2,
            'measure_collector_time': False,
            'byte_unit': 'byte',
            'urls': 'localhost http://localhost:80/server-status?auto',
        })

        expected_urls = {'localhost': 'http://localhost:80/server-status?auto'}

        self.assertEqual(self.collector.urls, expected_urls)

##########################################################################
if __name__ == "__main__":
    unittest.main()
