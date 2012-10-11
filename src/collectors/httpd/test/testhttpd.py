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
    def setUp(self):
        config = get_collector_config('HttpdCollector', {
            'interval': '10',
            'url':      ''
        })

        self.collector = HttpdCollector(config, None)

        self.HTTPResponse = TestHTTPResponse()

        httplib.HTTPConnection.request = Mock(return_value=True)
        httplib.HTTPConnection.getresponse = Mock(
            return_value=self.HTTPResponse)

    @patch.object(Collector, 'publish')
    def test_should_work_with_synthetic_data(self, publish_mock):
        with patch.object(TestHTTPResponse,
                          'read',
                          Mock(return_value=self.getFixture(
                              'server-status-fake-1').getvalue())):
            self.collector.collect()

        self.assertPublishedMany(publish_mock, {})

        with patch.object(TestHTTPResponse,
                          'read',
                          Mock(return_value=self.getFixture(
                              'server-status-fake-2').getvalue())):
            self.collector.collect()

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
        with patch.object(TestHTTPResponse,
                          'read',
                          Mock(return_value=self.getFixture(
                              'server-status-live-1').getvalue())):
            self.collector.collect()

        self.assertPublishedMany(publish_mock, {})

        with patch.object(TestHTTPResponse,
                          'read',
                          Mock(return_value=self.getFixture(
                              'server-status-live-2').getvalue())):
            self.collector.collect()

        metrics = {
            'TotalAccesses': 8314,
            'ReqPerSec': 0,
            'BytesPerSec': 165,
            'BytesPerReq': 5418,
            'BusyWorkers': 9,
            'IdleWorkers': 0,
        }

        self.setDocExample(self.collector.__class__.__name__, metrics)
        self.assertPublishedMany(publish_mock, metrics)

################################################################################
if __name__ == "__main__":
    unittest.main()
