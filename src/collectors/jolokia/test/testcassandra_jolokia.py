#!/usr/bin/python
# coding=utf-8
##########################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import patch

from diamond.collector import Collector

from cassandra_jolokia import CassandraJolokiaCollector

##########################################################################


class TestCassandraJolokiaCollector(CollectorTestCase):

    def setUp(self):
        config = get_collector_config('CassandraJolokiaCollector', {})

        self.collector = CassandraJolokiaCollector(config, None)

    # Used for all the tests so the expected numbers are all the same.
    def fixture_a(self):
        values = [0] * 92
        values[30:56] = [3, 3, 1, 1, 8, 5, 6, 1, 6, 5, 3, 8, 9, 10, 7, 8, 7, 5,
                         5, 5, 3, 3, 2, 2, 2]
        return values

    def empty_fixture_values(self):
        return [0] * 91

    def expected_fixture_a_p(self, percentile_key):
        return {
            'p25': 192.0,
            'p50': 398.0,
            'p75': 824.0,
            'p95': 2050.0,
            'p99': 2952.0
        }[percentile_key]

    def test_import(self):
        self.assertTrue(CassandraJolokiaCollector)

    def test_should_compute_percentiles_accurately(self):
        ninety_offsets = self.collector.create_offsets(90)
        percentile_value = self.collector.compute_percentile(
            ninety_offsets, self.fixture_a(), 50)
        self.assertEqual(percentile_value, 398.0)

    def test_should_compute_percentiles_accurately_when_empty(self):
        ninety_offsets = self.collector.create_offsets(90)
        self.assertEqual(self.collector.compute_percentile(
            ninety_offsets, self.empty_fixture_values(), 50), 0.0)
        self.assertEqual(self.collector.compute_percentile(
            ninety_offsets, self.empty_fixture_values(), 95), 0.0)
        self.assertEqual(self.collector.compute_percentile(
            ninety_offsets, self.empty_fixture_values(), 99), 0.0)

    @patch.object(Collector, 'publish')
    def test_should_not_collect_non_histogram_attributes(self, publish_mock):
        self.collector.interpret_bean_with_list(
            'RecentReadLatencyMicros', self.fixture_a())
        self.assertPublishedMany(publish_mock, {})

    @patch.object(Collector, 'publish')
    def test_should_collect_metrics_histogram_attributes(self, publish_mock):
        self.collector.interpret_bean_with_list(
            'RecentReadLatencyHistogramMicros', self.fixture_a())
        self.assertPublishedMany(publish_mock, {
            'RecentReadLatencyHistogramMicros.p50':
            self.expected_fixture_a_p('p50'),
            'RecentReadLatencyHistogramMicros.p95':
            self.expected_fixture_a_p('p95'),
            'RecentReadLatencyHistogramMicros.p99':
            self.expected_fixture_a_p('p99')
        })

    @patch.object(Collector, 'publish')
    # db:columnfamily=HintsColumnFamily,keyspace=system,type=ColumnFamilies:
    def test_should_escape_histogram_attributes(self, publish_mock):
        test_bean = ','.join([
            'db:columnfamily=HintsColumnFamily',
            'keyspace=system',
            'type=ColumnFamilies:RecentReadLatencyHistogramMicros'
        ])
        self.collector.interpret_bean_with_list(test_bean, self.fixture_a())

        expected_base = '.'.join([
            'db.columnfamily_HintsColumnFamily',
            'keyspace_system',
            'type_ColumnFamilies',
            'RecentReadLatencyHistogramMicros'
        ])
        self.assertPublishedMany(publish_mock, {
            '.'.join([expected_base, 'p50']): self.expected_fixture_a_p('p50'),
            '.'.join([expected_base, 'p95']): self.expected_fixture_a_p('p95'),
            '.'.join([expected_base, 'p99']): self.expected_fixture_a_p('p99')
        })

    @patch.object(Collector, 'publish')
    def test_should_respect_percentiles_config(self, publish_mock):
        self.collector.update_config({
            'percentiles': ['25', '75']
        })
        self.collector.interpret_bean_with_list(
            'RecentReadLatencyHistogramMicros', self.fixture_a())
        self.assertPublishedMany(publish_mock, {
            'RecentReadLatencyHistogramMicros.p25':
            self.expected_fixture_a_p('p25'),
            'RecentReadLatencyHistogramMicros.p75':
            self.expected_fixture_a_p('p75'),
        })

    @patch.object(Collector, 'publish')
    def test_should_respect_histogram_regex_config(self, publish_mock):
        self.collector.update_config({
            'histogram_regex': '^WackyMetric'
        })
        self.collector.interpret_bean_with_list(
            'WackyMetricSeventeen', self.fixture_a())
        self.assertPublishedMany(publish_mock, {
            'WackyMetricSeventeen.p50':
            self.expected_fixture_a_p('p50'),
            'WackyMetricSeventeen.p95':
            self.expected_fixture_a_p('p95'),
            'WackyMetricSeventeen.p99':
            self.expected_fixture_a_p('p99')
        })

##########################################################################
if __name__ == "__main__":
    unittest.main()
