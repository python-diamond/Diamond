#!/usr/bin/python
# coding=utf-8
##########################################################################

import os
import time
import mock
from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from test import run_only
from mock import patch

from diamond.collector import Collector
from loggly import LogglyCollector

##########################################################################


def run_only_if_requirements_present(func):
    try:
        import requests
    except ImportError:
        requests = None
    try:
        import futures
    except ImportError:
        futures = None
    try:
        import bunch
    except ImportError:
        bunch = None
    return run_only(func,
                    lambda: all((module is not None
                                for module in [requests, futures, bunch])))


class TestLogglyCollector(CollectorTestCase):
    TEST_CONFIG = {
        'interval': 10,
        'subdomain': 'mocksub',
        'username': 'mockuser',
        'password': 'mockpass',
        'metric': {
            'testmetric': {
                'field': 'mock.field',
                'query': 'mock: query'
            },
            'countmetric': {
                'field': 'mock.field',
                'count': 'true',
                'query': 'mock: count_query'
            },
            'badmetric': {
                'field': 'mock.field',
                'count': 'true',
                'query': 'mock: bad'
            },
            'unauthorizedmetric': {
                'field': 'mock.field',
                'count': 'true',
                'query': 'mock: unauthorized'
            },
            'forbiddenmetric': {
                'field': 'mock.field',
                'count': 'true',
                'query': 'mock: forbidden'
            },
            'gonemetric': {
                'field': 'mock.field',
                'count': 'true',
                'query': 'mock: gone'
            },
            'serverrormetric': {
                'field': 'mock.field',
                'count': 'true',
                'query': 'mock: serverror'
            },
            'notimplementedmetric': {
                'field': 'mock.field',
                'count': 'true',
                'query': 'mock: not implemented'
            },
            'throttledmetric': {
                'field': 'mock.field',
                'count': 'true',
                'query': 'mock: throttled'
            },
            'timeoutmetric': {
                'field': 'mock.field',
                'query': 'mock: timeout'
            },
        }
    }

    def mocked_requests_get(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data

        recorded_responses = {
            'https://mocksub.loggly.com/apiv2/search?'
            'q=mock: query&from=-10s&until=now':
                MockResponse({'rsid': {'id': 1}}, 200),
            'https://mocksub.loggly.com/apiv2/search?'
            'q=mock: count_query&from=-10s&until=now':
                MockResponse({'rsid': {'id': 1}}, 200),
            'https://mocksub.loggly.com/apiv2/search?'
            'q=mock: bad&from=-10s&until=now':
                MockResponse({'rsid': {'id': 1}}, 400),
            'https://mocksub.loggly.com/apiv2/search?'
            'q=mock: unauthorized&from=-10s&until=now':
                MockResponse({'rsid': {'id': 1}}, 401),
            'https://mocksub.loggly.com/apiv2/search?'
            'q=mock: forbidden&from=-10s&until=now':
                MockResponse({'rsid': {'id': 1}}, 403),
            'https://mocksub.loggly.com/apiv2/search?'
            'q=mock: gone&from=-10s&until=now':
                MockResponse({'rsid': {'id': 1}}, 410),
            'https://mocksub.loggly.com/apiv2/search?'
            'q=mock: serverror&from=-10s&until=now':
                MockResponse({'rsid': {'id': 1}}, 500),
            'https://mocksub.loggly.com/apiv2/search?'
            'q=mock: not implemented&from=-10s&until=now':
                MockResponse({'rsid': {'id': 1}}, 501),
            'https://mocksub.loggly.com/apiv2/search?'
            'q=mock: throttled&from=-10s&until=now':
                MockResponse({'rsid': {'id': 1}}, 503),
            'https://mocksub.loggly.com/apiv2/search?'
            'q=mock: timeout&from=-10s&until=now':
                MockResponse({'rsid': {'id': 1}}, 504),
            'https://mocksub.loggly.com/apiv2/events?rsid=1':
                MockResponse({
                    'events': [{'timestamp': 1443092343,
                                'event': {'mock': {'field': 123.456}}}],
                    'total_events': 4}, 200)
        }
        try:
            return recorded_responses[args[1]]
        except:
            return MockResponse({}, 404)

    def setUp(self):
        config = get_collector_config('LogglyCollector',
                                      self.TEST_CONFIG)

        self.collector = LogglyCollector(config, None)

    def test_import(self):
        self.assertTrue(LogglyCollector)

    # @run_only_if_requirements_present
    @patch.object(Collector, 'publish_metric')
    def test(self, publish_mock):
        patch_requests_get = patch('requests.get',
                                   side_effect=self.mocked_requests_get)
        patch_requests_get.start()
        self.collector.collect()
        patch_requests_get.stop()

        published_metrics = {
            'testmetric.mock.field': (123.456, None),
            'countmetric.mock.field': (123.456, None),
            'countmetric.count': 4
        }
        unpublished_metrics = {
            'badmetric.mock.field': 0,
            'unauthorizedmetric.mock.field': 0,
            'forbiddenmetric.mock.field': 0,
            'gonemetric.mock.field': 0,
            'serverrormetric.mock.field': 0,
            'notimplementedmetric.mock.field': 0,
            'throttledmetric.mock.field': 0,
            'timeoutmetric.mock.field': 0,
            'testmetric.count': 0
        }

        self.assertPublishedMetricMany(publish_mock, published_metrics)
        self.assertUnpublishedMetricMany(publish_mock, unpublished_metrics)

##########################################################################
if __name__ == "__main__":
    unittest.main()
