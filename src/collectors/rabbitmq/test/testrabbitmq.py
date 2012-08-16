#!/usr/bin/python
# coding=utf-8
################################################################################

from test import *

from diamond.collector import Collector
from rabbitmq import RabbitMQCollector

################################################################################


class TestRabbitMQCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('RabbitMQCollector', {
            'host': 'localhost:55672',
            'user': 'guest',
            'password': 'password'
        })
        self.collector = RabbitMQCollector(config, None)

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

        self.setDocExample(self.collector.__class__.__name__, metrics)
        self.assertPublishedMany(publish_mock, metrics)

################################################################################
if __name__ == "__main__":
    unittest.main()
