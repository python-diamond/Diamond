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
        urlopen_mock = patch('urllib2.urlopen', Mock(
            return_value=self.getFixture('stats')))

        urlopen_mock.start()
        self.collector.collect()
        urlopen_mock.stop()

        metrics = {
            'http.current': 1,

            'indices.docs.count': 11968062,
            'indices.docs.deleted': 2692068,
            'indices.datastore.size': 22724243633,

            'process.cpu.percent': 58,

            'process.mem.resident': 5192126464,
            'process.mem.share': 11075584,
            'process.mem.virtual': 7109668864,

            'disk.reads.count': 55996,
            'disk.reads.size': 1235387392,
            'disk.writes.count': 5808198,
            'disk.writes.size': 23287275520,
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
