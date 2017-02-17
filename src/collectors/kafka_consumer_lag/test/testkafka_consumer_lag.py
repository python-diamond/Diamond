#!/usr/bin/python
# coding=utf-8
##########################################################################

from test import CollectorTestCase
from test import get_collector_config
from mock import patch, Mock

from diamond.collector import Collector
from kafka_consumer_lag import KafkaConsumerLagCollector

##########################################################################


class TestKafkaConsumerLagCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('KafkaConsumerLagCollector', {
            'consumer_groups': ['test_group']
        })

        self.collector = KafkaConsumerLagCollector(config, None)

    def test_import(self):
        self.assertTrue(KafkaConsumerLagCollector)

    @patch.object(Collector, 'publish')
    def test_should_publish_gpu_stat(self, publish_mock):
        output_mock = Mock(
            return_value=(self.getFixture('consumer_lag_check').getvalue(), '')
        )
        collector_mock = patch.object(
            KafkaConsumerLagCollector,
            'run_command',
            output_mock
        )

        collector_mock.start()
        self.collector.collect()
        collector_mock.stop()

        metrics = {
            'stage_nginx_access.nginx_access.0': 0,
            'stage_nginx_access.nginx_access.1': 2,
            'stage_nginx_access.nginx_access.2': 0,
            'stage_nginx_access.nginx_access.3': 0,
            'stage_nginx_access.nginx_access.4': 0,
            'stage_nginx_access.nginx_access.5': 0,
            'stage_nginx_access.nginx_access.6': 0,
            'stage_nginx_access.nginx_access.7': 52,
            'stage_nginx_access.nginx_access.8': 0,
            'stage_nginx_access.nginx_access.9': 0,
            'stage_nginx_access.nginx_access.10': 0
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)\


    @patch.object(Collector, 'publish')
    def test_should_publish_gpu_stat(self, publish_mock):
        self.collector.config.update({
            'zookeeper':
                ['192.168.1.101:2181', '192.168.1.102:2181/dev/test-01']
        })
        output_mock = Mock(
            return_value=(self.getFixture('consumer_lag_check').getvalue(), '')
        )
        collector_mock = patch.object(
            KafkaConsumerLagCollector,
            'run_command',
            output_mock
        )

        collector_mock.start()
        self.collector.collect()
        collector_mock.stop()

        metrics = {
            'dev_test_01.stage_nginx_access.nginx_access.0': 0,
            'dev_test_01.stage_nginx_access.nginx_access.1': 2,
            'dev_test_01.stage_nginx_access.nginx_access.2': 0,
            'dev_test_01.stage_nginx_access.nginx_access.3': 0,
            'dev_test_01.stage_nginx_access.nginx_access.4': 0,
            'dev_test_01.stage_nginx_access.nginx_access.5': 0,
            'dev_test_01.stage_nginx_access.nginx_access.6': 0,
            'dev_test_01.stage_nginx_access.nginx_access.7': 52,
            'dev_test_01.stage_nginx_access.nginx_access.8': 0,
            'dev_test_01.stage_nginx_access.nginx_access.9': 0,
            'dev_test_01.stage_nginx_access.nginx_access.10': 0
        }
        self.assertPublishedMany(publish_mock, metrics)
