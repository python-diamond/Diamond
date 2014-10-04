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
        except ImportError:
            pyrabbit = None
    pred = lambda: pyrabbit is not None
    return run_only(func, pred)


class TestRabbitMQCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('RabbitMQCollector', {
            'host': 'localhost:55672',
            'user': 'guest',
            'password': 'password',
            'queues_ignored': ['^ignored', ],
            'cluster': True,
        })
        self.collector = RabbitMQCollector(config, None)

    def test_import(self):
        self.assertTrue(RabbitMQCollector)

    def http_mock(self, path, method):
        overview_data = {
            'node': 'rabbit@localhost',
        }
        node_health = {
            'fd_used': 1,
            'fd_total': 2,
            'mem_used': 2,
            'mem_limit': 4,
            'sockets_used': 1,
            'sockets_total': 2,
            'disk_free_limit': 1,
            'disk_free': 1,
            'proc_used': 1,
            'proc_total': 1,
            'partitions': [],
        }
        nodes = [1, 2, 3]
        if path == 'overview':
            return overview_data
        elif path == 'nodes/rabbit@localhost':
            return node_health
        elif path == 'nodes':
            return nodes

    @run_only_if_pyrabbit_is_available
    @patch('pyrabbit.api.Client')
    @patch('pyrabbit.http.HTTPClient')
    @patch.object(Collector, 'publish')
    def test_should_publish_nested_keys(self, publish_mock, httpclient,
                                        client_mock):
        client = Mock()
        queue_data = [{
            'more_keys': {'nested_key': 1},
            'key': 2,
            'string': 'str',
            'name': 'test_queue'
            },
            {
                'name': 'ignored',
                'more_keys': {'nested_key': 1},
                'key': 2,
                'string': 'str',
            },
        ]
        overview_data = {
            'more_keys': {'nested_key': 3},
            'key': 4,
            'string': 'string',
        }
        client_mock.return_value = client
        client.get_queues.return_value = [queue_data]
        client.get_overview.return_value = overview_data

        httpclient = Mock()
        httpclient.do_call.return_value = self.http_mock

        self.collector.collect()

        client.get_queues.assert_called_once_with(None)
        client.get_overview.assert_called_once_with()
        httpclient.do_call.assert_called_once_with('nodes', 'GET')

        metrics = {
            'queues.test_queue.more_keys.nested_key': 1,
            'queues.test_queue.key': 2,
            'more_keys.nested_key': 3,
            'key': 4,
            'health.fd_used': 1,
            'health.fd_total': 2,
            'health.mem_used': 2,
            'health.mem_limit': 4,
            'health.sockets_used': 1,
            'health.sockets_total': 2,
            'health.disk_free_limit': 1,
            'health.disk_free': 1,
            'health.proc_used': 1,
            'health.proc_total': 1,
            'cluster.partitions': 0,
            'cluster.nodes': 3
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

################################################################################
if __name__ == "__main__":
    unittest.main()
