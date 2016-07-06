#!/usr/bin/python
# coding=utf-8
##########################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import Mock, call
from mock import patch

from diamond.collector import Collector

from aerospike import AerospikeCollector

##########################################################################


class TestAerospikeCollector(CollectorTestCase):

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

        mockTelnet = Mock(**{'read_until.return_value':
                             self.getFixture('latency').getvalue()})

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
            'latency.reads.1ms': 1.75,
            'latency.reads.8ms': 0.67,
            'latency.reads.64ms': 0.36,
            'latency.reads.ops': 54839.0,
            'latency.writes_master.1ms': 11.69,
            'latency.writes_master.8ms': 2.54,
            'latency.writes_master.64ms': 2.06,
            'latency.writes_master.ops': 8620.1,
            'latency.proxy.1ms': 1.35,
            'latency.proxy.8ms': 6.88,
            'latency.proxy.64ms': 1.37,
            'latency.proxy.ops': 320.1,
            'latency.udf.1ms': 1.47,
            'latency.udf.8ms': 8.64,
            'latency.udf.64ms': 4.11,
            'latency.udf.ops': 140.33,
            'latency.query.1ms': 3.44,
            'latency.query.8ms': 2.74,
            'latency.query.64ms': 1.04,
            'latency.query.ops': 84.12,
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
            'read_until.return_value':
            self.getFixture('statistics').getvalue()
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
            'statistics.total-bytes-memory': 345744867328,
            'statistics.total-bytes-disk': 8801921007616,
            'statistics.used-bytes-memory': 126136727552,
            'statistics.used-bytes-disk': 2457236328960,
            'statistics.free-pct-memory': 63,
            'statistics.free-pct-disk': 72,
            'statistics.data-used-bytes-memory': 0,
            'statistics.index-used-bytes-memory': 126136727552,
            'statistics.cluster_size': 13,
            'statistics.objects': 1970886368,
            'statistics.client_connections': 3014,
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
            'read_until.return_value':
            self.getFixture('throughput').getvalue()
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
            'throughput.reads': 54563.9,
            'throughput.writes_master': 9031.0,
            'throughput.proxy': 884.3,
            'throughput.udf': 42.3,
            'throughput.query': 64.3,
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
                self.getFixture('namespaces').getvalue(),
                self.getFixture('namespace_foo').getvalue(),
                self.getFixture('namespace_bar').getvalue(),
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
                call('namespaces\n'),
                call('namespace/foo\n'),
                call('namespace/bar\n'),
            ],
        )

        metrics = {
            'namespace.foo.objects': 1841012935,
            'namespace.foo.evicted-objects': 0,
            'namespace.foo.expired-objects': 167836937,
            'namespace.foo.used-bytes-memory': 117824827840,
            'namespace.foo.data-used-bytes-memory': 0,
            'namespace.foo.index-used-bytes-memory': 117824827840,
            'namespace.foo.used-bytes-disk': 2401223781248,
            'namespace.foo.memory-size': 343597383680,
            'namespace.foo.total-bytes-memory': 343597383680,
            'namespace.foo.total-bytes-disk': 8801921007616,
            'namespace.foo.migrate-tx-partitions-initial': 651,
            'namespace.foo.migrate-tx-partitions-remaining': 651,
            'namespace.foo.migrate-rx-partitions-initial': 651,
            'namespace.foo.migrate-rx-partitions-remaining': 651,
            'namespace.foo.available_pct': 60,
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
                self.getFixture('namespaces').getvalue(),
                self.getFixture('namespace_bar').getvalue(),
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
                call('namespaces\n'),
                call('namespace/bar\n'),
            ],
        )

##########################################################################
if __name__ == "__main__":
    unittest.main()
