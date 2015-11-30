#!/usr/bin/python
# coding=utf-8
##########################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import Mock
from mock import patch

from diamond.collector import Collector
from rabbitmq import RabbitMQCollector

##########################################################################


class TestRabbitMQCollector(CollectorTestCase):

    def setUp(self):
        config = get_collector_config('RabbitMQCollector', {
            'host': 'localhost:55672',
            'user': 'guest',
            'password': 'password',
            'queues_ignored': '^ignored',
            'cluster': True,
        })
        self.collector = RabbitMQCollector(config, None)

    def test_import(self):
        self.assertTrue(RabbitMQCollector)

    @patch('rabbitmq.RabbitMQClient')
    @patch.object(Collector, 'publish')
    def test_should_publish_nested_keys(self, publish_mock, client_mock):
        client = Mock()
        queue_data = [{
            'more_keys': {'nested_key': 1},
            'key': 2,
            'string': 'str',
            'name': 'test_queue'
        }, {
            'name': 'ignored',
            'more_keys': {'nested_key': 1},
            'key': 2,
            'string': 'str',
        }]
        overview_data = {
            'node': 'rabbit@localhost',
            'more_keys': {'nested_key': 3},
            'key': 4,
            'string': 'string',
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
        client_mock.return_value = client
        client.get_queues.return_value = queue_data
        client.get_overview.return_value = overview_data
        client.get_nodes.return_value = [1, 2, 3]
        client.get_node.return_value = node_health

        self.collector.collect()

        client.get_queues.assert_called_once_with(None)
        client.get_nodes.assert_called_once_with()
        client.get_node.assert_called_once_with('rabbit@localhost')

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

    @patch('rabbitmq.RabbitMQClient')
    @patch.object(Collector, 'publish')
    def test_opt_should_replace_dots(self, publish_mock, client_mock):
        self.collector.config['replace_dot'] = '_'
        client = Mock()
        queue_data = [{
            'more_keys': {'nested_key': 1},
            'key': 2,
            'string': 'str',
            'name': 'test.queue'
        }, {
            'name': 'ignored',
            'more_keys': {'nested_key': 1},
            'key': 2,
            'string': 'str',
        }]
        overview_data = {
            'node': 'rabbit@localhost',
            'more_keys': {'nested_key': 3},
            'key': 4,
            'string': 'string',
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
        client_mock.return_value = client
        client.get_queues.return_value = queue_data
        client.get_overview.return_value = overview_data
        client.get_nodes.return_value = [1, 2, 3]
        client.get_node.return_value = node_health

        self.collector.collect()

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

        self.collector.config['replace_dot'] = False

##########################################################################
if __name__ == "__main__":
    unittest.main()
