#!/usr/bin/python
# coding=utf-8
##########################################################################

import json

from collections import namedtuple

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import Mock
from mock import patch

from diamond.collector import Collector

from dropwizard import DropwizardCollector

##########################################################################


MockRequest = namedtuple('MockRequest', 'status_code json')


class TestDropwizardCollector(CollectorTestCase):

    def setUp(self):
        config = get_collector_config('DropwizardCollector', {})

        self.collector = DropwizardCollector(config, None)

    def test_import(self):
        self.assertTrue(DropwizardCollector)

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        return_test_json = lambda: json.load(self.getFixture('stats'))
        patch_request = patch('requests.get',
                              Mock(return_value=MockRequest(
                                        status_code=200,
                                        json=return_test_json
                                   )))

        patch_request.start()
        self.collector.collect()
        patch_request.stop()

        # below metrics are not comprehensive
        published_metrics = {
            'gauges.jvm.attribute.uptime.value': 76207123,
            'gauges.jvm.memory.non-heap.init.value': 7667712,
            'gauges.jvm.memory.non-heap.max.value': -1,
            'gauges.jvm.memory.non-heap.usage.value': -77628320,
            'gauges.jvm.memory.non-heap.used.value': 77628320,
            'gauges.jvm.memory.total.init.value': 263520256,
            'gauges.jvm.memory.total.max.value': 4085252095,
            'gauges.jvm.memory.total.used.value': 121300576,
            'gauges.jvm.threads.blocked.count.value': 0,
            'gauges.jvm.threads.count.value': 26,
            'counters.io.dropwizard.jetty.MutableServletContextHandler.active-dispatches.count': 0,
            'counters.io.dropwizard.jetty.MutableServletContextHandler.active-requests.count': 0,
            'counters.io.dropwizard.jetty.MutableServletContextHandler.active-suspended.count': 0,
            'meters.io.dropwizard.jetty.MutableServletContextHandler.1xx-responses.count': 0,
            'meters.io.dropwizard.jetty.MutableServletContextHandler.1xx-responses.mean_rate': 0,
            'meters.io.dropwizard.jetty.MutableServletContextHandler.2xx-responses.count': 0,
            'meters.io.dropwizard.jetty.MutableServletContextHandler.2xx-responses.mean_rate': 0,
            'meters.io.dropwizard.jetty.MutableServletContextHandler.3xx-responses.count': 2,
            'meters.io.dropwizard.jetty.MutableServletContextHandler.3xx-responses.mean_rate': 2.624538034865841e-05,
            'meters.io.dropwizard.jetty.MutableServletContextHandler.4xx-responses.count': 7,
            'meters.io.dropwizard.jetty.MutableServletContextHandler.4xx-responses.mean_rate': 9.18588313665478e-05,
            'meters.io.dropwizard.jetty.MutableServletContextHandler.5xx-responses.count': 0,
            'meters.io.dropwizard.jetty.MutableServletContextHandler.5xx-responses.mean_rate': 0,
            'timers.io.dropwizard.jetty.MutableServletContextHandler.connect-requests.count': 0,
            'timers.io.dropwizard.jetty.MutableServletContextHandler.connect-requests.mean':  0,
            'timers.io.dropwizard.jetty.MutableServletContextHandler.delete-requests.count': 0,
            'timers.io.dropwizard.jetty.MutableServletContextHandler.delete-requests.mean':  0,
            'timers.io.dropwizard.jetty.MutableServletContextHandler.dispatches.count': 9,
            'timers.io.dropwizard.jetty.MutableServletContextHandler.dispatches.mean': 0.0015657667280344347,
            'timers.io.dropwizard.jetty.MutableServletContextHandler.get-requests.count': 9,
            'timers.io.dropwizard.jetty.MutableServletContextHandler.get-requests.mean': 0.001565766728034435,

        }
        excluded_metrics = {
            'gauges.io.dropwizard.jetty.MutableServletContextHandler.percent-4xx-1m.value': 1,
            'gauges.jvm.attribute.name.value': 'some-name',
            'counters.TimeBoundHealthCheck-pool-%d.running.count': 0,
            'meters.TimeBoundHealthCheck-pool-%d.created.count': 0,
            'timers.io.dropwizard.jetty.MutableServletContextHandler.connect-requests.mean_rate': 0
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=published_metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, published_metrics)
        self.assertUnpublishedMany(publish_mock, excluded_metrics)

    @patch.object(Collector, 'publish')
    def test_should_fail_empty_response(self, publish_mock):
        return_test_json = lambda: json.load(self.getFixture('stats_blank'))
        patch_request = patch('requests.get',
                              Mock(return_value=MockRequest(
                                        status_code=200,
                                        json=return_test_json
                                   )))

        patch_request.start()
        self.collector.collect()
        patch_request.stop()

        self.assertPublishedMany(publish_mock, {})

    @patch.object(Collector, 'publish')
    def test_should_fail_on_404(self, publish_mock):
        patch_request = patch('requests.get',
                              Mock(return_value=MockRequest(
                                        status_code=404,
                                        json=lambda:{}
                                   )))
        patch_request.start()
        self.collector.collect()
        patch_request.stop()

        self.assertPublishedMany(publish_mock, {})

#########################################################################
if __name__ == "__main__":
    unittest.main()
