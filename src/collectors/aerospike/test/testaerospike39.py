#!/usr/bin/python
# coding=utf-8
##########################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import call
from test import Mock
from test import patch

from diamond.collector import Collector

from aerospike import AerospikeCollector

##########################################################################


class TestAerospike39Collector(CollectorTestCase):

    def bootStrap(self, custom_config={}):
        config = get_collector_config('AerospikeCollector', custom_config)

        self.collector = AerospikeCollector(config, None)

    def test_import(self):
        self.assertTrue(AerospikeCollector)

    @patch.object(Collector, 'publish')
    @patch.object(Collector, 'publish_gauge')
    @patch.object(Collector, 'publish_counter')
    def test_latency(self, publish_counter_mock,
                     publish_gauge_mock, publish_mock):

        mockTelnet = Mock(**{
            'read_until.side_effect':
            [
                "3.9",
                self.getFixture('v3.9/latency').getvalue(),
            ]
        })

        patch_Telnet = patch('telnetlib.Telnet', Mock(return_value=mockTelnet))

        patch_Telnet.start()
        self.bootStrap(custom_config={
            'latency': True,
            'statistics': False,
            'throughput': False,
            'namespaces': False,
        })

        self.collector.collect()
        patch_Telnet.stop()

        mockTelnet.read_until.assert_any_call('\n', 1)

        metrics = {
            'latency.foo.read.1ms': 1.00,
            'latency.foo.read.8ms': 3.00,
            'latency.foo.read.64ms': 5.00,
            'latency.foo.read.ops': 2206.8,
            'latency.bar.read.1ms': 2.00,
            'latency.bar.read.8ms': 4.00,
            'latency.bar.read.64ms': 6.00,
            'latency.bar.read.ops': 4206.8,
            'latency.foo.write.1ms': 1.28,
            'latency.foo.write.8ms': 3.01,
            'latency.foo.write.64ms': 5.01,
            'latency.foo.write.ops': 1480.4,
            'latency.bar.write.1ms': 2.28,
            'latency.bar.write.8ms': 4.01,
            'latency.bar.write.64ms': 6.01,
            'latency.bar.write.ops': 2480.4,
        }

        self.assertPublishedMany(
            [publish_mock,
             publish_gauge_mock,
             publish_counter_mock,
             ],
            metrics,
        )

    @patch.object(Collector, 'publish')
    @patch.object(Collector, 'publish_gauge')
    @patch.object(Collector, 'publish_counter')
    def test_statistics(self, publish_counter_mock,
                        publish_gauge_mock, publish_mock):

        mockTelnet = Mock(**{
            'read_until.side_effect':
            [
                "3.9",
                self.getFixture('v3.9/statistics').getvalue(),
                ]
        })

        patch_Telnet = patch('telnetlib.Telnet', Mock(return_value=mockTelnet))

        patch_Telnet.start()
        self.bootStrap(custom_config={
            'latency': False,
            'statistics': True,
            'throughput': False,
            'namespaces': False,
        })

        self.collector.collect()
        patch_Telnet.stop()

        mockTelnet.read_until.assert_any_call('\n', 1)

        metrics = {
            'statistics.objects': 6816672,
            'statistics.cluster_size': 3,
            'statistics.system_free_mem_pct': 87,
            'statistics.client_connections': 51,
            'statistics.scans_active': 0,
        }

        self.assertPublishedMany(
            [publish_mock,
             publish_gauge_mock,
             publish_counter_mock,
             ],
            metrics,
        )

    @patch.object(Collector, 'publish')
    @patch.object(Collector, 'publish_gauge')
    @patch.object(Collector, 'publish_counter')
    def test_throughput(self, publish_counter_mock,
                        publish_gauge_mock, publish_mock):

        mockTelnet = Mock(**{
            'read_until.side_effect':
            [
                "3.9",
                self.getFixture('v3.9/throughput').getvalue(),
                ]
        })

        patch_Telnet = patch('telnetlib.Telnet', Mock(return_value=mockTelnet))

        patch_Telnet.start()
        self.bootStrap(custom_config={
            'latency': False,
            'statistics': False,
            'throughput': True,
            'namespaces': False,
        })

        self.collector.collect()
        patch_Telnet.stop()

        mockTelnet.read_until.assert_any_call('\n', 1)

        metrics = {
            'throughput.foo.read': 2089.3,
            'throughput.foo.write': 1478.6,
            'throughput.bar.read': 3089.3,
            'throughput.bar.write': 3478.6,
        }

        self.assertPublishedMany(
            [publish_mock,
             publish_gauge_mock,
             publish_counter_mock,
             ],
            metrics,
        )

    @patch.object(Collector, 'publish')
    @patch.object(Collector, 'publish_gauge')
    @patch.object(Collector, 'publish_counter')
    def test_namespaces(self, publish_counter_mock,
                        publish_gauge_mock, publish_mock):

        mockTelnet = Mock(**{
            'read_until.side_effect':
            [
                "3.9",
                self.getFixture('v3.9/namespaces').getvalue(),
                self.getFixture('v3.9/namespace_foo').getvalue(),
                self.getFixture('v3.9/namespace_bar').getvalue(),
                ],
        })

        patch_Telnet = patch('telnetlib.Telnet', Mock(return_value=mockTelnet))

        patch_Telnet.start()
        self.bootStrap(custom_config={
            'latency': False,
            'statistics': False,
            'throughput': False,
            'namespaces': True,
        })

        self.collector.collect()
        patch_Telnet.stop()

        mockTelnet.read_until.assert_any_call('\n', 1)
        mockTelnet.write.assert_has_calls(
            [
                call('version\n'),
                call('namespaces\n'),
                call('namespace/foo\n'),
                call('namespace/bar\n'),
            ],
        )

        metrics = {
            'namespace.foo.objects': 6831009,
            'namespace.foo.memory_free_pct': 86,
            'namespace.foo.memory-size': 21474836480,
            'namespace.foo.client_read_error': 0,
            'namespace.foo.device_free_pct': 88,
            'namespace.bar.objects': 5831009,
            'namespace.bar.memory_free_pct': 76,
            'namespace.bar.memory-size': 31474836480,
            'namespace.bar.client_read_error': 0,
            'namespace.bar.device_free_pct': 88,
        }

        self.assertPublishedMany(
            [publish_mock,
             publish_gauge_mock,
             publish_counter_mock,
             ],
            metrics,
        )

    def test_namespace_whitelist(self):

        mockTelnet = Mock(**{
            'read_until.side_effect':
            [
                "3.9",
                self.getFixture('v3.9/namespaces').getvalue(),
                self.getFixture('v3.9/namespace_bar').getvalue(),
            ],
        })

        patch_Telnet = patch('telnetlib.Telnet', Mock(return_value=mockTelnet))

        patch_Telnet.start()
        self.bootStrap(custom_config={
            'latency': False,
            'statistics': False,
            'throughput': False,
            'namespaces': True,
            'namespaces_whitelist': ['bar'],
        })

        self.collector.collect()
        patch_Telnet.stop()

        mockTelnet.read_until.assert_any_call('\n', 1)
        mockTelnet.write.assert_has_calls(
            [
                call('version\n'),
                call('namespaces\n'),
                call('namespace/bar\n'),
            ],
        )

##########################################################################
if __name__ == "__main__":
    unittest.main()
