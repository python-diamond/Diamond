#!/usr/bin/python
# coding=utf-8
################################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import patch

from diamond.collector import Collector
from numa import NumaCollector

################################################################################


class TestExampleCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('NumaCollector', {
            'interval': 10
        })

        self.collector = NumaCollector(config, None)

    def test_import(self):
        self.assertTrue(NumaCollector)

    @patch.object(Collector, 'publish')
    def test(self, publish_mock):
        self.collector.collect()

        metrics = {
            'node_0_free_MB':  42,
            'node_0_size_MB':  402
        }

        self.setDocNuma(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

################################################################################
if __name__ == "__main__":
    unittest.main()
