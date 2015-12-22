#!/usr/bin/python
# coding=utf-8
##########################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import call, patch

from diamond.collector import Collector

from solr import SolrCollector

##########################################################################


class TestSolrCollector(CollectorTestCase):

    def setUp(self):
        config = get_collector_config('SolrCollector', {})
        self.collector = SolrCollector(config, None)

    def test_import(self):
        self.assertTrue(SolrCollector)

    @patch('urllib2.urlopen')
    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock, urlopen_mock):
        returns = [self.getFixture('cores'),
                   self.getFixture('ping'),
                   self.getFixture('stats'),
                   self.getFixture('system')]
        urlopen_mock.side_effect = lambda *args: returns.pop(0)

        self.collector.collect()

        metrics = {
            'response.QueryTime': 5,
            'response.Status': 0,

            "core.maxDoc": 321,
            "core.numDocs": 184,
            "core.warmupTime": 0,

            "queryhandler.standard.requests": 3,
            "queryhandler.standard.errors": 0,
            "queryhandler.standard.timeouts": 0,
            "queryhandler.standard.totalTime": 270,
            "queryhandler.standard.avgTimePerRequest": 90,
            "queryhandler.standard.avgRequestsPerSecond": 0.00016776958,

            "queryhandler.update.requests": 0,
            "queryhandler.update.errors": 0,
            "queryhandler.update.timeouts": 0,
            "queryhandler.update.totalTime": 0,
            "queryhandler.update.avgRequestsPerSecond": 0,

            "updatehandler.commits": 0,
            "updatehandler.autocommits": 0,
            "updatehandler.optimizes": 0,
            "updatehandler.rollbacks": 0,
            "updatehandler.docsPending": 0,
            "updatehandler.adds": 0,
            "updatehandler.errors": 0,
            "updatehandler.cumulative_adds": 0,
            "updatehandler.cumulative_errors": 0,

            'cache.fieldValueCache.lookups': 0,
            'cache.fieldValueCache.hits': 0,
            'cache.fieldValueCache.hitratio': 0.0,
            'cache.fieldValueCache.inserts': 0,
            'cache.fieldValueCache.evictions': 0,
            'cache.fieldValueCache.size': 0,
            'cache.fieldValueCache.warmupTime': 0,
            'cache.fieldValueCache.cumulative_lookups': 0,
            'cache.fieldValueCache.cumulative_hits': 0,
            'cache.fieldValueCache.cumulative_hitratio': 0.0,
            'cache.fieldValueCache.cumulative_inserts': 0,
            'cache.fieldValueCache.cumulative_evictions': 0,

            'cache.filterCache.lookups': 0,
            'cache.filterCache.hits': 0,
            'cache.filterCache.hitratio': 0.0,
            'cache.filterCache.inserts': 0,
            'cache.filterCache.evictions': 0,
            'cache.filterCache.size': 0,
            'cache.filterCache.warmupTime': 0,
            'cache.filterCache.cumulative_lookups': 0,
            'cache.filterCache.cumulative_hits': 0,
            'cache.filterCache.cumulative_hitratio': 0.0,
            'cache.filterCache.cumulative_inserts': 0,
            'cache.filterCache.cumulative_evictions': 0,

            'cache.documentCache.lookups': 0,
            'cache.documentCache.hits': 0,
            'cache.documentCache.hitratio': 0.0,
            'cache.documentCache.inserts': 0,
            'cache.documentCache.evictions': 0,
            'cache.documentCache.size': 0,
            'cache.documentCache.warmupTime': 0,
            'cache.documentCache.cumulative_lookups': 0,
            'cache.documentCache.cumulative_hits': 0,
            'cache.documentCache.cumulative_hitratio': 0.0,
            'cache.documentCache.cumulative_inserts': 0,
            'cache.documentCache.cumulative_evictions': 0,

            'cache.queryResultCache.lookups': 3,
            'cache.queryResultCache.hits': 2,
            'cache.queryResultCache.hitratio': 0.66,
            'cache.queryResultCache.inserts': 1,
            'cache.queryResultCache.evictions': 0,
            'cache.queryResultCache.size': 1,
            'cache.queryResultCache.warmupTime': 0,
            'cache.queryResultCache.cumulative_lookups': 3,
            'cache.queryResultCache.cumulative_hits': 2,
            'cache.queryResultCache.cumulative_hitratio': 0.66,
            'cache.queryResultCache.cumulative_inserts': 1,
            'cache.queryResultCache.cumulative_evictions': 0,

            'jvm.mem.free': 42.7,
            'jvm.mem.total': 61.9,
            'jvm.mem.max': 185.6,
            'jvm.mem.used': 19.2,
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics)
        self.assertPublishedMany(publish_mock, metrics)

        urlopen_mock.assert_has_calls([
            call(
                'http://localhost:8983/solr/admin/cores?action=STATUS&wt=json'),
            call('http://localhost:8983/solr/admin/ping?wt=json'),
            call('http://localhost:8983/solr/admin/mbeans?stats=true&wt=json'),
            call('http://localhost:8983/solr/admin/system?stats=true&wt=json')
        ])

    @patch('urllib2.urlopen')
    @patch.object(Collector, 'publish')
    def test_should_fail_gracefully(self, publish_mock, urlopen_mock):
        urlopen_mock.return_value = self.getFixture('stats_blank')

        self.collector.collect()

        self.assertPublishedMany(publish_mock, {})
        urlopen_mock.assert_called_once_with(
            'http://localhost:8983/solr/admin/cores?action=STATUS&wt=json')


##########################################################################
if __name__ == "__main__":
    unittest.main()
