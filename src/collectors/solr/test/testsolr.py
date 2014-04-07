#!/usr/bin/python
# coding=utf-8
################################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import Mock
from mock import patch

from diamond.collector import Collector

from solr import SolrCollector

################################################################################


class TestSolrCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('SolrCollector', {})
        self.collector = SolrCollector(config, None)

    def test_import(self):
        self.assertTrue(SolrCollector)

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        returns = [self.getFixture('cores'),
                   self.getFixture('ping'),
                   self.getFixture('stats'),
                   self.getFixture('system')]
        urlopen_mock = patch('urllib2.urlopen', Mock(
            side_effect=lambda *args: returns.pop(0)))

        urlopen_mock.start()
        self.collector.collect()
        urlopen_mock.stop()

        metrics = {
            'solr.response.QueryTime': 5,
            'solr.response.Status': 0,

            "solr.core.maxDoc": 321,
            "solr.core.numDocs": 184,
            "solr.core.warmupTime": 0,

            "solr.queryhandler.standard.requests": 3,
            "solr.queryhandler.standard.errors": 0,
            "solr.queryhandler.standard.timeouts": 0,
            "solr.queryhandler.standard.totalTime": 270,
            "solr.queryhandler.standard.avgTimePerRequest": 90,
            "solr.queryhandler.standard.avgRequestsPerSecond": 0.00016776958,

            "solr.queryhandler.update.requests": 0,
            "solr.queryhandler.update.errors": 0,
            "solr.queryhandler.update.timeouts": 0,
            "solr.queryhandler.update.totalTime": 0,
            "solr.queryhandler.update.avgRequestsPerSecond": 0,

            "solr.updatehandler.commits": 0,
            "solr.updatehandler.autocommits": 0,
            "solr.updatehandler.optimizes": 0,
            "solr.updatehandler.rollbacks": 0,
            "solr.updatehandler.docsPending": 0,
            "solr.updatehandler.adds": 0,
            "solr.updatehandler.errors": 0,
            "solr.updatehandler.cumulative_adds": 0,
            "solr.updatehandler.cumulative_errors": 0,

            'solr.cache.fieldValueCache.lookups': 0,
            'solr.cache.fieldValueCache.hits': 0,
            'solr.cache.fieldValueCache.hitratio': 0.0,
            'solr.cache.fieldValueCache.inserts': 0,
            'solr.cache.fieldValueCache.evictions': 0,
            'solr.cache.fieldValueCache.size': 0,
            'solr.cache.fieldValueCache.warmupTime': 0,
            'solr.cache.fieldValueCache.cumulative_lookups': 0,
            'solr.cache.fieldValueCache.cumulative_hits': 0,
            'solr.cache.fieldValueCache.cumulative_hitratio': 0.0,
            'solr.cache.fieldValueCache.cumulative_inserts': 0,
            'solr.cache.fieldValueCache.cumulative_evictions': 0,

            'solr.cache.filterCache.lookups': 0,
            'solr.cache.filterCache.hits': 0,
            'solr.cache.filterCache.hitratio': 0.0,
            'solr.cache.filterCache.inserts': 0,
            'solr.cache.filterCache.evictions': 0,
            'solr.cache.filterCache.size': 0,
            'solr.cache.filterCache.warmupTime': 0,
            'solr.cache.filterCache.cumulative_lookups': 0,
            'solr.cache.filterCache.cumulative_hits': 0,
            'solr.cache.filterCache.cumulative_hitratio': 0.0,
            'solr.cache.filterCache.cumulative_inserts': 0,
            'solr.cache.filterCache.cumulative_evictions': 0,

            'solr.cache.documentCache.lookups': 0,
            'solr.cache.documentCache.hits': 0,
            'solr.cache.documentCache.hitratio': 0.0,
            'solr.cache.documentCache.inserts': 0,
            'solr.cache.documentCache.evictions': 0,
            'solr.cache.documentCache.size': 0,
            'solr.cache.documentCache.warmupTime': 0,
            'solr.cache.documentCache.cumulative_lookups': 0,
            'solr.cache.documentCache.cumulative_hits': 0,
            'solr.cache.documentCache.cumulative_hitratio': 0.0,
            'solr.cache.documentCache.cumulative_inserts': 0,
            'solr.cache.documentCache.cumulative_evictions': 0,

            'solr.cache.queryResultCache.lookups': 3,
            'solr.cache.queryResultCache.hits': 2,
            'solr.cache.queryResultCache.hitratio': 0.66,
            'solr.cache.queryResultCache.inserts': 1,
            'solr.cache.queryResultCache.evictions': 0,
            'solr.cache.queryResultCache.size': 1,
            'solr.cache.queryResultCache.warmupTime': 0,
            'solr.cache.queryResultCache.cumulative_lookups': 3,
            'solr.cache.queryResultCache.cumulative_hits': 2,
            'solr.cache.queryResultCache.cumulative_hitratio': 0.66,
            'solr.cache.queryResultCache.cumulative_inserts': 1,
            'solr.cache.queryResultCache.cumulative_evictions': 0,

            'solr.jvm.mem.free': 42.7,
            'solr.jvm.mem.total': 61.9,
            'solr.jvm.mem.max': 185.6,
            'solr.jvm.mem.used': 19.2,
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics)
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
