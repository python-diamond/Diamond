#!/usr/bin/python
# coding=utf-8
##########################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import Mock
from mock import patch

from diamond.collector import Collector

from elasticsearch import ElasticSearchCollector

##########################################################################


class TestElasticSearchCollector(CollectorTestCase):

    def setUp(self):
        config = get_collector_config('ElasticSearchCollector', {})

        self.collector = ElasticSearchCollector(config, None)

    def test_import(self):
        self.assertTrue(ElasticSearchCollector)

    def test_new__instances_default(self):
        config = get_collector_config('ElasticSearchCollector', {})
        self.collector = ElasticSearchCollector(config, None)
        self.assertEqual(self.collector.instances, {'': ('127.0.0.1', 9200)})

    def test_new__instances_single(self):
        config = get_collector_config('ElasticSearchCollector', {
            'instances': 'bla'})
        self.collector = ElasticSearchCollector(config, None)
        self.assertEqual(self.collector.instances, {'default': ('bla', 9200)})

    def test_new__instances_multi(self):
        config = get_collector_config('ElasticSearchCollector', {
            'instances': [
                'something',
                'foo@1234',
                'bar@bla:1234',
            ]})
        self.collector = ElasticSearchCollector(config, None)
        self.assertEqual(self.collector.instances, {
            'default': ('something', 9200),
            'foo': ('1234', 9200),
            'bar': ('bla', 1234),
        })

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        returns = [
            self.getFixture('stats'),
            self.getFixture('cluster_stats'),
            self.getFixture('indices_stats'),
        ]
        urlopen_mock = patch('urllib2.urlopen', Mock(
            side_effect=lambda *args: returns.pop(0)))

        self.collector.config['cluster'] = True

        urlopen_mock.start()
        self.collector.collect()
        urlopen_mock.stop()

        # check how many fixtures were consumed
        self.assertEqual(urlopen_mock.new.call_count, 3)

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

        # check how many fixtures were consumed
        self.assertEqual(urlopen_mock.new.call_count, 2)

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
            self.getFixture('stats0.90'),
            self.getFixture('indices_stats'),
        ]
        urlopen_mock = patch('urllib2.urlopen', Mock(
            side_effect=lambda *args: returns.pop(0)))

        urlopen_mock.start()
        self.collector.collect()
        urlopen_mock.stop()

        # check how many fixtures were consumed
        self.assertEqual(urlopen_mock.new.call_count, 2)

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

    @patch.object(Collector, 'publish')
    def test_multi_instances_with_real_data(self, publish_mock):
        config = get_collector_config('ElasticSearchCollector', {
            'instances': [
                'esprodata01@10.10.10.201:9200',
                'esprodata02@10.10.10.202:9200',
            ]})
        self.collector = ElasticSearchCollector(config, None)
        self.assertEqual(len(self.collector.instances), 2)

        returns = [
            self.getFixture('stats'),
            self.getFixture('indices_stats'),
            self.getFixture('stats2'),
            self.getFixture('indices_stats2'),
        ]
        urlopen_mock = patch('urllib2.urlopen', Mock(
            side_effect=lambda *args: returns.pop(0)))

        urlopen_mock.start()
        self.collector.collect()
        urlopen_mock.stop()

        # check how many fixtures were consumed
        self.assertEqual(urlopen_mock.new.call_count, 4)

        metrics = {
            'esprodata01.http.current': 1,
            'esprodata02.http.current': 2,

            'esprodata01.indices.docs.count': 11968062,
            'esprodata02.indices.docs.count': 11968000,

            'esprodata01.thread_pool.generic.threads': 1,
            'esprodata02.thread_pool.generic.threads': 2,

            'esprodata01.jvm.mem.pools.Par_Survivor_Space.max': 8716288,
            'esprodata02.jvm.mem.pools.Par_Survivor_Space.max': 8710000,

            'esprodata01.indices._all.docs.count': 4,
            'esprodata02.indices._all.docs.count': 8,
        }

        self.assertPublishedMany(publish_mock, metrics)

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_1_7_data(self, publish_mock):
        returns = [
            self.getFixture('stats1.7'),
            self.getFixture('indices_stats'),
        ]
        urlopen_mock = patch('urllib2.urlopen', Mock(
            side_effect=lambda *args: returns.pop(0)))

        urlopen_mock.start()
        self.collector.collect()
        urlopen_mock.stop()

        # check how many fixtures were consumed
        self.assertEqual(urlopen_mock.new.call_count, 2)

        # test some 1.7 specific stats
        metrics = {
            'segments.count': 7,
            'segments.mem.size': 75726,
            'segments.index_writer.mem.size': 0,
            'segments.index_writer.mem.max_size': 469762048,
            'segments.version_map.mem.size': 0,
            'segments.fixed_bit_set.mem.size': 0
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

##########################################################################
if __name__ == "__main__":
    unittest.main()
