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
    return True
    # return run_only(func,
    #                 lambda: all((module is not None
    #                             for module in [requests, futures, bunch])))


class TestLogglyCollector(CollectorTestCase):
    TEST_CONFIG = {
        'interval': 10,
        'metric': {
            'testmetric': {
                'subdomain': 'mocksub',
                'username': 'mockuser',
                'password': 'mockpass',
                'field': 'mock.field',
                'query': 'mock: query'
            },
            'countmetric': {
                'subdomain': 'mocksub',
                'username': 'mockuser',
                'password': 'mockpass',
                'count': 'true',
                'query': 'mock: count_query'
            }
        }
    }

    def setUp(self):
        config = get_collector_config('LogglyCollector',
                                      self.TEST_CONFIG)

        self.collector = LogglyCollector(config, None)

    def test_import(self):
        self.assertTrue(LogglyCollector)

    # @run_only_if_requirements_present
    @patch.object(LogglyCollector, 'publish')
    def test(self, publish_mock):
        def mocked_requests_get(*args, **kwargs):
            class MockResponse:
                def __init__(self, json_data, status_code):
                    self.json_data = json_data
                    self.status_code = status_code

                def json(self):
                    return self.json_data

            recorded_responses = {
                'https://mocksub.loggly.com/apiv2/search?q=mock: query&from=-10s&until=now': MockResponse({'rsid': {'id': 1}}, 200),
                'https://mocksub.loggly.com/apiv2/search?q=mock: count_query&from=-10s&until=now': MockResponse({'rsid': {'id': 2}}, 200),
                'https://mocksub.loggly.com/apiv2/events?rsid=1': MockResponse({'events': [{'timestamp': 1443092343, 'event': {'mock': {'field': 123.456}}}]}, 200),
                'https://mocksub.loggly.com/apiv2/events?rsid=2': MockResponse({'total_events': 4}, 200)
            }
            try:
                return recorded_responses[args[0]]
            except:
                return MockResponse({}, 404)

        patch_requests_get = patch('requests.get',
                                   side_effect=mocked_requests_get)
        patch_requests_get.start()
        self.collector.collect()
        patch_requests_get.stop()

        metrics = {
            'testmetric.mock.field': 123.456,
            'countmetric.count': 4
        }
        self.assertPublishedMany(publish_mock, metrics)

##########################################################################
if __name__ == "__main__":
    unittest.main()
