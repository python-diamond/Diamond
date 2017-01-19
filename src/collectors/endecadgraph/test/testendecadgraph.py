#!/usr/bin/python
# coding=utf-8
##########################################################################

from test import CollectorTestCase
from test import get_collector_config
from mock import patch

from diamond.collector import Collector
from endecadgraph import EndecaDgraphCollector


class TestEndecaDgraphCollector(CollectorTestCase):

    def setUp(self):
        config = get_collector_config('EndecaDgraphCollector', {
        })
        self.collector = EndecaDgraphCollector(config, None)

    def test_import(self):
        self.assertTrue(EndecaDgraphCollector)

    @patch('urllib2.urlopen')
    @patch.object(Collector, 'publish')
    def test_real_data(self, publish_mock, urlopen_mock):
        urlopen_mock.return_value = self.getFixture('data1.xml')
        self.collector.collect()
        self.assertPublishedMany(publish_mock, {})

        urlopen_mock.return_value = self.getFixture('data2.xml')
        self.collector.collect()

        # assert with a random selection (instead of 1000+)
        metrics = {
            'statistics.cache_section.main_cache.'
            'aggregatedrecordcount.entry_count': 3957,
            'statistics.cache_section.main_cache.'
            'dval_bincount.entry_count': 4922448,
            'statistics.hot_spot_analysis.'
            'content_spotlighting_performance.min': 0.0209961,
            'statistics.hot_spot_analysis.'
            'insertion_sort_time.avg': 0.00523964,
            'statistics.hot_spot_analysis.'
            'ordinal_insertion_sort_time.n': 1484793,
            'statistics.search_performance_analysis.'
            'qconj_lookupphr.min': 0.000976562,
            'statistics.updates.update_latency.'
            'commit.audit_stat_calculation_time_resume_.n': 0,
        }
        self.assertPublishedMany(publish_mock, metrics)

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
