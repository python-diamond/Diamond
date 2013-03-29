#!/usr/bin/python
# coding=utf-8
################################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from test import run_only
from mock import Mock
from mock import patch, call

from diamond.collector import Collector
from redisstat import RedisCollector

################################################################################


def run_only_if_redis_is_available(func):
    """Decorator for checking if python-redis is available.
    Note: this test will be silently skipped if python-redis is missing.
    """
    try:
        import redis
        redis  # workaround for pyflakes issue #13
    except ImportError:
        redis = None
    pred = lambda: redis is not None
    return run_only(func, pred)


class TestRedisCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('RedisCollector', {
            'interval': '1',
            'databases': 1,
        })

        self.collector = RedisCollector(config, None)

    def test_import(self):
        self.assertTrue(RedisCollector)

    @run_only_if_redis_is_available
    @patch.object(Collector, 'publish')
    def test_real_data(self, publish_mock):

        data_1 = {'pubsub_channels': 0,
                  'used_memory_peak_human': '700.71K',
                  'bgrewriteaof_in_progress': 0,
                  'connected_slaves': 0,
                  'uptime_in_days': 0,
                  'multiplexing_api': 'epoll',
                  'lru_clock': 954113,
                  'last_save_time': 1351718385,
                  'redis_version': '2.4.10',
                  'redis_git_sha1': 0,
                  'gcc_version': '4.4.6',
                  'connected_clients': 1,
                  'keyspace_misses': 0,
                  'used_memory': 726144,
                  'vm_enabled': 0,
                  'used_cpu_user_children': '0.00',
                  'used_memory_peak': 717528,
                  'role': 'master',
                  'total_commands_processed': 1,
                  'latest_fork_usec': 0,
                  'loading': 0,
                  'used_memory_rss': 7254016,
                  'total_connections_received': 1,
                  'pubsub_patterns': 0,
                  'aof_enabled': 0,
                  'used_cpu_sys': '0.02',
                  'used_memory_human': '709.12K',
                  'used_cpu_sys_children': '0.00',
                  'blocked_clients': 0,
                  'used_cpu_user': '0.00',
                  'client_biggest_input_buf': 0,
                  'arch_bits': 64,
                  'mem_fragmentation_ratio': '9.99',
                  'expired_keys': 0,
                  'evicted_keys': 0,
                  'bgsave_in_progress': 0,
                  'client_longest_output_list': 0,
                  'mem_allocator': 'jemalloc-2.2.5',
                  'process_id': 3020,
                  'uptime_in_seconds': 32,
                  'changes_since_last_save': 0,
                  'redis_git_dirty': 0,
                  'keyspace_hits': 0
                  }
        data_2 = {'pubsub_channels': 1,
                  'used_memory_peak_human': '1700.71K',
                  'bgrewriteaof_in_progress': 4,
                  'connected_slaves': 2,
                  'uptime_in_days': 1,
                  'multiplexing_api': 'epoll',
                  'lru_clock': 5954113,
                  'last_save_time': 51351718385,
                  'redis_version': '2.4.10',
                  'redis_git_sha1': 0,
                  'gcc_version': '4.4.6',
                  'connected_clients': 100,
                  'keyspace_misses': 670,
                  'used_memory': 1726144,
                  'vm_enabled': 0,
                  'used_cpu_user_children': '2.00',
                  'used_memory_peak': 1717528,
                  'role': 'master',
                  'total_commands_processed': 19764,
                  'latest_fork_usec': 8,
                  'loading': 0,
                  'used_memory_rss': 17254016,
                  'total_connections_received': 18764,
                  'pubsub_patterns': 0,
                  'aof_enabled': 0,
                  'used_cpu_sys': '0.05',
                  'used_memory_human': '1709.12K',
                  'used_cpu_sys_children': '0.09',
                  'blocked_clients': 8,
                  'used_cpu_user': '0.09',
                  'client_biggest_input_buf': 40,
                  'arch_bits': 64,
                  'mem_fragmentation_ratio': '0.99',
                  'expired_keys': 0,
                  'evicted_keys': 0,
                  'bgsave_in_progress': 0,
                  'client_longest_output_list': 0,
                  'mem_allocator': 'jemalloc-2.2.5',
                  'process_id': 3020,
                  'uptime_in_seconds': 95732,
                  'changes_since_last_save': 759,
                  'redis_git_dirty': 0,
                  'keyspace_hits': 5700
                  }

        patch_collector = patch.object(RedisCollector, '_get_info',
                                       Mock(return_value=data_1))
        patch_time = patch('time.time', Mock(return_value=10))

        patch_collector.start()
        patch_time.start()
        self.collector.collect()
        patch_collector.stop()
        patch_time.stop()

        self.assertPublishedMany(publish_mock, {})

        patch_collector = patch.object(RedisCollector, '_get_info',
                                       Mock(return_value=data_2))
        patch_time = patch('time.time', Mock(return_value=20))

        patch_collector.start()
        patch_time.start()
        self.collector.collect()
        patch_collector.stop()
        patch_time.stop()

        metrics = {'6379.process.uptime': 95732,
                   '6379.pubsub.channels': 1,
                   '6379.slaves.connected': 2,
                   '6379.process.connections_received': 18764,
                   '6379.clients.longest_output_list': 0,
                   '6379.process.commands_processed': 19764,
                   '6379.last_save.changes_since': 759,
                   '6379.memory.external_view': 17254016,
                   '6379.memory.fragmentation_ratio': 0.99,
                   '6379.last_save.time': 51351718385,
                   '6379.clients.connected': 100,
                   '6379.clients.blocked': 8,
                   '6379.pubsub.patterns': 0,
                   '6379.cpu.parent.user': 0.09,
                   '6379.last_save.time_since': -51351718365,
                   '6379.memory.internal_view': 1726144,
                   '6379.cpu.parent.sys': 0.05,
                   '6379.keyspace.misses': 670,
                   '6379.keys.expired': 0,
                   '6379.keys.evicted': 0,
                   '6379.keyspace.hits': 5700,
                   }

        self.assertPublishedMany(publish_mock, metrics)

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])

    @run_only_if_redis_is_available
    @patch.object(Collector, 'publish')
    def test_hostport_or_instance_config(self, publish_mock):

        testcases = {
            'default': {
                'config': {},  # test default settings
                'calls': [call('6379', 'localhost', 6379, None)],
            },
            'host_set': {
                'config': {'host': 'myhost'},
                'calls': [call('6379', 'myhost', 6379, None)],
            },
            'port_set': {
                'config': {'port': 5005},
                'calls': [call('5005', 'localhost', 5005, None)],
            },
            'hostport_set': {
                'config': {'host': 'megahost', 'port': 5005},
                'calls': [call('5005', 'megahost', 5005, None)],
            },
            'instance_1_host': {
                'config': {'instances': ['nick@myhost']},
                'calls': [call('nick', 'myhost', 6379, None)],
            },
            'instance_1_port': {
                'config': {'instances': ['nick@:9191']},
                'calls': [call('nick', 'localhost', 9191, None)],
            },
            'instance_1_hostport': {
                'config': {'instances': ['nick@host1:8765']},
                'calls': [call('nick', 'host1', 8765, None)],
            },
            'instance_2': {
                'config': {'instances': ['foo@hostX', 'bar@:1000']},
                'calls': [
                    call('foo', 'hostX', 6379, None),
                    call('bar', 'localhost', 1000, None)
                ],
            },
            'old_and_new': {
                'config': {
                    'host': 'myhost',
                    'port': 1234,
                    'instances': [
                        'foo@hostX',
                        'bar@:1000',
                        'hostonly',
                        ':1234'
                    ]
                },
                'calls': [
                    call('foo', 'hostX', 6379, None),
                    call('bar', 'localhost', 1000, None),
                    call('6379', 'hostonly', 6379, None),
                    call('1234', 'localhost', 1234, None),
                ],
            },
        }

        for testname, data in testcases.items():
            config = get_collector_config('RedisCollector', data['config'])

            collector = RedisCollector(config, None)

            mock = Mock(return_value={}, name=testname)
            patch_c = patch.object(RedisCollector, 'collect_instance', mock)

            patch_c.start()
            collector.collect()
            patch_c.stop()

            expected_call_count = len(data['calls'])
            self.assertEqual(mock.call_count, expected_call_count,
                             msg='[%s] mock.calls=%d != expected_calls=%d' %
                             (testname, mock.call_count, expected_call_count))
            for exp_call in data['calls']:
                # Test expected calls 1 by 1,
                # because self.instances is a dict (=random order)
                mock.assert_has_calls(exp_call)

    @run_only_if_redis_is_available
    @patch.object(Collector, 'publish')
    def test_key_naming_when_using_instances(self, publish_mock):

        config_data = {
            'instances': [
                'nick1@host1:1111',
                'nick2@:2222',
                'nick3@host3',
                'bla'
            ]
        }
        get_info_data = {
            'total_connections_received': 200,
            'total_commands_processed': 100,
        }
        expected_calls = [
            call('nick1.process.connections_received', 200, precision=0,
                 metric_type='GAUGE'),
            call('nick1.process.commands_processed', 100, precision=0,
                 metric_type='GAUGE'),
            call('nick2.process.connections_received', 200, precision=0,
                 metric_type='GAUGE'),
            call('nick2.process.commands_processed', 100, precision=0,
                 metric_type='GAUGE'),
            call('nick3.process.connections_received', 200, precision=0,
                 metric_type='GAUGE'),
            call('nick3.process.commands_processed', 100, precision=0,
                 metric_type='GAUGE'),
            call('6379.process.connections_received', 200, precision=0,
                 metric_type='GAUGE'),
            call('6379.process.commands_processed', 100, precision=0,
                 metric_type='GAUGE'),
        ]

        config = get_collector_config('RedisCollector', config_data)
        collector = RedisCollector(config, None)

        patch_c = patch.object(RedisCollector, '_get_info',
                               Mock(return_value=get_info_data))

        patch_c.start()
        collector.collect()
        patch_c.stop()

        self.assertEqual(publish_mock.call_count, len(expected_calls))
        for exp_call in expected_calls:
            # Test expected calls 1 by 1,
            # because self.instances is a dict (=random order)
            publish_mock.assert_has_calls(exp_call)


################################################################################
if __name__ == "__main__":
    unittest.main()
