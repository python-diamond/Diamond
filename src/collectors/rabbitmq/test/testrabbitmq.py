#!/usr/bin/python
# coding=utf-8
################################################################################

import sys
from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from test import run_only
from mock import Mock
from mock import patch

from diamond.collector import Collector
from rabbitmq import RabbitMQCollector

################################################################################


def run_only_if_pyrabbit_is_available(func):
    pyrabbit = None
    if sys.version_info > (2, 5):
        try:
            import pyrabbit
            pyrabbit  # workaround for pyflakes issue #13
        except ImportError:
            pyrabbit = None
    pred = lambda: pyrabbit is not None
    return run_only(func, pred)


class TestRabbitMQCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('RabbitMQCollector', {
            'host': 'localhost:55672',
            'user': 'guest',
            'password': 'password'
        })
        self.collector = RabbitMQCollector(config, None)

    def test_import(self):
        self.assertTrue(RabbitMQCollector)

    @run_only_if_pyrabbit_is_available
    @patch('pyrabbit.api.Client')
    @patch.object(Collector, 'publish')
    def test_should_publish_nested_keys(self, publish_mock, client_mock):
        client = Mock()
        queue_data = {
            'more_keys': {'nested_key': 1},
            'key': 2,
            'string': 'str',
            'name': 'test_queue'
        }
        overview_data = {
            'more_keys': {'nested_key': 3},
            'key': 4,
            'string': 'string',
        }
        client_mock.return_value = client
        client.get_queues.return_value = [queue_data]
        client.get_overview.return_value = overview_data

        self.collector.collect()

        client.get_queues.assert_called_once_with()
        client.get_overview.assert_called_once_with()
        metrics = {
            'queues.test_queue.more_keys.nested_key': 1,
            'queues.test_queue.key': 2,
            'more_keys.nested_key': 3,
            'key': 4
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

################################################################################
if __name__ == "__main__":
    unittest.main()
