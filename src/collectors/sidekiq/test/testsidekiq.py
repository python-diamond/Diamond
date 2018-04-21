#!/usr/bin/python
# coding=utf-8
##########################################################################
import redis

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from test import run_only
from mock import Mock
from mock import patch

from diamond.collector import Collector
from sidekiq import SidekiqCollector

##########################################################################


def run_only_if_redis_is_available(func):
    """Decorator for checking if python-redis is available.
    Note: this test will be silently skipped if python-redis is missing.
    """
    try:
        import redis
    except ImportError:
        redis = None
    return run_only(func, lambda: redis is not None)


class TestSidekiqCollector(CollectorTestCase):

    def setUp(self):
        config = get_collector_config('SidekiqWebCollector', {
            'password': 'TEST_PASSWORD'
        })

        self.collector = SidekiqCollector(config, None)

    def test_import(self):
        self.assertTrue(SidekiqCollector)

    @run_only_if_redis_is_available
    @patch.object(Collector, 'publish')
    def test_sidekiq_queue(self, publish_mock):
        self.collector.config.update({
            'ports': '6379'
        })
        patch_collector = patch.object(
            redis.Redis, 'smembers', Mock(return_value=['queue_1'])
        )
        length_collector = patch.object(
            redis.Redis, 'llen', Mock(return_value=123)
        )
        zcard_collector = patch.object(
            redis.Redis, 'zcard', Mock(return_value=100)
        )

        patch_collector.start()
        length_collector.start()
        zcard_collector.start()

        self.collector.collect()

        patch_collector.stop()
        length_collector.stop()
        zcard_collector.stop()

        metrics = {
            'queue.6379.0.queue_1': 123,
            'queue.6379.0.retry': 100,
            'queue.6379.0.schedule': 100
        }

        self.assertPublishedMany(publish_mock, metrics)

    @run_only_if_redis_is_available
    @patch.object(Collector, 'publish')
    def test_sidekiq_queue_with_databases(self, publish_mock):
        self.collector.config.update({
            'ports': ['6379', '6380'],
            'sentinel_ports': ['26379', '26380'],
            'databases': 2
        })
        patch_collector = patch.object(
            redis.Redis, 'smembers', Mock(return_value=['queue_1'])
        )
        length_collector = patch.object(
            redis.Redis, 'llen', Mock(return_value=123)
        )
        zcard_collector = patch.object(
            redis.Redis, 'zcard', Mock(return_value=100)
        )

        patch_collector.start()
        length_collector.start()
        zcard_collector.start()

        self.collector.collect()

        patch_collector.stop()
        length_collector.stop()
        zcard_collector.stop()

        metrics = {
            'queue.6379.0.queue_1': 123,
            'queue.6379.0.retry': 100,
            'queue.6379.0.schedule': 100,
            'queue.6380.0.queue_1': 123,
            'queue.6380.0.retry': 100,
            'queue.6380.0.schedule': 100,
            'queue.6379.1.queue_1': 123,
            'queue.6379.1.retry': 100,
            'queue.6379.1.schedule': 100,
            'queue.6380.1.queue_1': 123,
            'queue.6380.1.retry': 100,
            'queue.6380.1.schedule': 100
        }

        self.assertPublishedMany(publish_mock, metrics)

    @run_only_if_redis_is_available
    @patch.object(Collector, 'publish')
    def test_sidekiq_queue_with_cluster_prefix(self, publish_mock):
        self.collector.config.update({
            'cluster_prefix': 'test-sidekiq',
            'sentinel_ports': '63790'
        })
        patch_collector = patch.object(
            redis.Redis, 'smembers', Mock(return_value=['queue_1', 'queue_2'])
        )
        length_collector = patch.object(
            redis.Redis, 'llen', Mock(return_value=123)
        )
        zcard_collector = patch.object(
            redis.Redis, 'zcard', Mock(return_value=100)
        )

        patch_collector.start()
        length_collector.start()
        zcard_collector.start()

        self.collector.collect()

        patch_collector.stop()
        length_collector.stop()
        zcard_collector.stop()

        metrics = {
            'queue.test-sidekiq.6379.0.queue_1': 123,
            'queue.test-sidekiq.6379.0.schedule': 100,
            'queue.test-sidekiq.6379.0.retry': 100
        }
        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

##########################################################################
if __name__ == "__main__":
    unittest.main()
