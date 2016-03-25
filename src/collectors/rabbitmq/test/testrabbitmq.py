#!/usr/bin/python
# coding=utf-8
##########################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import Mock
from mock import patch
from mock import call

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
        client.get_vhost_names.return_value = ['/']

        self.collector.collect()

        client.get_queues.assert_called_once_with('/')
        client.get_queue.assert_not_called()
        client.get_nodes.assert_called_once_with()
        client.get_node.assert_called_once_with('rabbit@localhost')
        client.get_vhost_names.assert_called_once_with()

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
        client.get_vhost_names.return_value = ['/']

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

    @patch('rabbitmq.RabbitMQClient')
    @patch.object(Collector, 'publish')
    def test_opt_should_replace_slashes(self, publish_mock, client_mock):
        self.collector.config['replace_slash'] = '_'
        client = Mock()
        queue_data = [{
            'more_keys': {'nested_key': 1},
            'key': 2,
            'string': 'str',
            'name': 'test/queue'
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
        client.get_vhost_names.return_value = ['/']

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

        self.collector.config['replace_slash'] = False

    @patch('rabbitmq.RabbitMQClient')
    @patch.object(Collector, 'publish')
    def test_opt_individual_queues(self, publish_mock, client_mock):
        self.collector.config['query_individual_queues'] = True
        self.collector.config['queues'] = 'queue1 queue2 queue3 queue4'
        client = Mock()
        queue_data = {
            'vhost1': {
                'queue1': {
                    'name': 'queue1',
                    'key': 1,
                    'string': 'str',
                },
                'queue2': {
                    'name': 'queue2',
                    'key': 2,
                    'string': 'str',
                },
                'ignored': {
                    'name': 'ignored',
                    'key': 3,
                    'string': 'str',
                },
            },
            'vhost2': {
                'queue3': {
                    'name': 'queue3',
                    'key': 4,
                    'string': 'str',
                },
                'queue4': {
                    'name': 'queue4',
                    'key': 5,
                    'string': 'str',
                },
                'ignored': {
                    'name': 'ignored',
                    'key': 6,
                    'string': 'str',
                }
            }
        }
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
        client_mock.return_value = client
        client.get_queue.side_effect = lambda v, q: queue_data.get(v).get(q)
        client.get_overview.return_value = overview_data
        client.get_nodes.return_value = [1, 2, 3]
        client.get_node.return_value = node_health
        client.get_vhost_names.return_value = ['vhost1', 'vhost2']

        self.collector.collect()

        client.get_queues.assert_not_called()
        client.get_nodes.assert_called_once_with()
        client.get_node.assert_called_once_with('rabbit@localhost')
        client.get_vhost_names.assert_called_once_with()
        client.get_queue.assert_has_calls([
            call('vhost1', 'queue1'),
            call('vhost1', 'queue2'),
            call('vhost2', 'queue3'),
            call('vhost2', 'queue4'),
        ], any_order=True)

        metrics = {
            'queues.queue1.key': 1,
            'queues.queue2.key': 2,
            'queues.queue3.key': 4,
            'queues.queue4.key': 5,
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

        self.collector.config['query_individual_queues'] = False
        self.collector.config['queues'] = ''

    @patch('rabbitmq.RabbitMQClient')
    @patch.object(Collector, 'publish')
    def test_opt_vhost_individual_queues(self, publish_mock, client_mock):
        self.collector.config['query_individual_queues'] = True
        self.collector.config['vhosts'] = {
            'vhost1': 'queue1 queue2',
            'vhost2': 'queue3 queue4'
        }
        client = Mock()
        queue_data = {
            'vhost1': {
                'queue1': {
                    'name': 'queue1',
                    'key': 1,
                    'string': 'str',
                },
                'queue2': {
                    'name': 'queue2',
                    'key': 2,
                    'string': 'str',
                },
                'ignored': {
                    'name': 'ignored',
                    'key': 3,
                    'string': 'str',
                },
            },
            'vhost2': {
                'queue3': {
                    'name': 'queue3',
                    'key': 4,
                    'string': 'str',
                },
                'queue4': {
                    'name': 'queue4',
                    'key': 5,
                    'string': 'str',
                },
                'ignored': {
                    'name': 'ignored',
                    'key': 6,
                    'string': 'str',
                }
            }
        }
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
        client_mock.return_value = client
        client.get_queue.side_effect = lambda v, q: queue_data.get(v).get(q)
        client.get_overview.return_value = overview_data
        client.get_nodes.return_value = [1, 2, 3]
        client.get_node.return_value = node_health
        client.get_vhost_names.return_value = ['vhost1', 'vhost2']

        self.collector.collect()

        client.get_queues.assert_not_called()
        client.get_nodes.assert_called_once_with()
        client.get_node.assert_called_once_with('rabbit@localhost')
        client.get_vhost_names.assert_called_once_with()
        client.get_queue.assert_has_calls([
            call('vhost1', 'queue1'),
            call('vhost1', 'queue2'),
            call('vhost2', 'queue3'),
            call('vhost2', 'queue4'),
        ], any_order=True)

        metrics = {
            'vhosts.vhost1.queues.queue1.key': 1,
            'vhosts.vhost1.queues.queue2.key': 2,
            'vhosts.vhost2.queues.queue3.key': 4,
            'vhosts.vhost2.queues.queue4.key': 5,
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

        self.collector.config['query_individual_queues'] = False
        del self.collector.config['vhosts']

##########################################################################
if __name__ == "__main__":
    unittest.main()
