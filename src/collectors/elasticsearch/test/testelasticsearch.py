#!/usr/bin/python
# coding=utf-8
################################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import Mock
from mock import patch

from diamond.collector import Collector

from elasticsearch import ElasticSearchCollector

################################################################################


class TestElasticSearchCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('ElasticSearchCollector', {})

        self.collector = ElasticSearchCollector(config, None)

    def test_import(self):
        self.assertTrue(ElasticSearchCollector)

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        returns = [self.getFixture('stats'), self.getFixture('indices_stats')]
        urlopen_mock = patch('urllib2.urlopen', Mock(
            side_effect=lambda *args: returns.pop(0)))

        urlopen_mock.start()
        self.collector.collect()
        urlopen_mock.stop()

        metrics = {
            'http.current': 1,

            'indices.docs.count': 11968062,
            'indices.docs.deleted': 2692068,
            'indices.datastore.size': 22724243633,

            'indices._all.docs.count': 4,
            'indices._all.docs.deleted': 0,
            'indices._all.datastore.size': 2674,

            'indices.test.docs.count': 4,
            'indices.test.docs.deleted': 0,
            'indices.test.datastore.size': 2674,

            'process.cpu.percent': 58,

            'process.mem.resident': 5192126464,
            'process.mem.share': 11075584,
            'process.mem.virtual': 7109668864,

            'disk.reads.count': 55996,
            'disk.reads.size': 1235387392,
            'disk.writes.count': 5808198,
            'disk.writes.size': 23287275520,

            'thread_pool.generic.threads': 1,

            'network.tcp.active_opens': 2299,

            'jvm.mem.pools.CMS_Old_Gen.used': 530915016,
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data_logstash_mode(self, publish_mock):
        returns = [
            self.getFixture('stats'),
            self.getFixture('logstash_indices_stats'),
        ]
        urlopen_mock = patch('urllib2.urlopen', Mock(
            side_effect=lambda *args: returns.pop(0)))

        self.collector.config['logstash_mode'] = True

        urlopen_mock.start()
        self.collector.collect()
        urlopen_mock.stop()

        # Omit all non-indices metrics, since those were already
        # checked in previous test.
        metrics = {
            'indices.docs.count': 11968062,
            'indices.docs.deleted': 2692068,
            'indices.datastore.size': 22724243633,

            'indices._all.docs.count': 35856619,
            'indices._all.docs.deleted': 0,
            'indices._all.datastore.size': 21903813340,

            'indices._all.get.exists_time_in_millis': 0,
            'indices._all.get.exists_total': 0,
            'indices._all.get.missing_time_in_millis': 0,
            'indices._all.get.missing_total': 0,
            'indices._all.get.time_in_millis': 0,
            'indices._all.get.total': 0,
            'indices._all.indexing.delete_time_in_millis': 0,
            'indices._all.indexing.delete_total': 0,
            'indices._all.indexing.index_time_in_millis': 29251475,
            'indices._all.indexing.index_total': 35189321,
            'indices._all.search.fetch_time_in_millis': 6962,
            'indices._all.search.fetch_total': 4084,
            'indices._all.search.query_time_in_millis': 41211,
            'indices._all.search.query_total': 4266,
            'indices._all.store.throttle_time_in_millis': 0,

            'indices.logstash-adm-syslog.indexes_in_group': 3,

            'indices.logstash-adm-syslog.datastore.size': 21903813340,
            'indices.logstash-adm-syslog.docs.count': 35856619,
            'indices.logstash-adm-syslog.docs.deleted': 0,
            'indices.logstash-adm-syslog.get.exists_time_in_millis': 0,
            'indices.logstash-adm-syslog.get.exists_total': 0,
            'indices.logstash-adm-syslog.get.missing_time_in_millis': 0,
            'indices.logstash-adm-syslog.get.missing_total': 0,
            'indices.logstash-adm-syslog.get.time_in_millis': 0,
            'indices.logstash-adm-syslog.get.total': 0,
            'indices.logstash-adm-syslog.indexing.delete_time_in_millis': 0,
            'indices.logstash-adm-syslog.indexing.delete_total': 0,
            'indices.logstash-adm-syslog.indexing.index_time_in_millis': 29251475,  # NOQA
            'indices.logstash-adm-syslog.indexing.index_total': 35189321,
            'indices.logstash-adm-syslog.search.fetch_time_in_millis': 6962,
            'indices.logstash-adm-syslog.search.fetch_total': 4084,
            'indices.logstash-adm-syslog.search.query_time_in_millis': 41211,
            'indices.logstash-adm-syslog.search.query_total': 4266,
            'indices.logstash-adm-syslog.store.throttle_time_in_millis': 0,
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_0_90_data(self, publish_mock):
        returns = [
            self.getFixture('stats0.90'), self.getFixture('indices_stats')]
        urlopen_mock = patch('urllib2.urlopen', Mock(
            side_effect=lambda *args: returns.pop(0)))

        urlopen_mock.start()
        self.collector.collect()
        urlopen_mock.stop()

        # test some 0.90 specific stats
        metrics = {
            'cache.filter.size': 1700,
            'cache.filter.evictions': 9,
            'cache.id.size': 98,
            'fielddata.size': 1448,
            'fielddata.evictions': 12,
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

    @patch.object(Collector, 'publish')
    def test_should_fail_gracefully(self, publish_mock):
        urlopen_mock = patch('urllib2.urlopen', Mock(
                             return_value=self.getFixture('stats_blank')))

        urlopen_mock.start()
        self.collector.collect()
        urlopen_mock.stop()

        self.assertPublishedMany(publish_mock, {})

################################################################################
if __name__ == "__main__":
    unittest.main()
