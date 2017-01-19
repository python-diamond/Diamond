#!/usr/bin/python
# coding=utf-8

###############################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import patch

from diamond.collector import Collector
from onewire import OneWireCollector

###############################################################################


class TestOneWireCollector(CollectorTestCase):

    def setUp(self):
        config = get_collector_config('OneWireCollector', {
            'owfs': self.getFixturePath('.'),
            'scan': {'temperature': 't'},
            'id:28.2F702A010000': {'presure': 'p11'}})
        self.collector = OneWireCollector(config, None)

    def test_import(self):
        self.assertTrue(OneWireCollector)

    @patch.object(Collector, 'publish')
    def test(self, publish_mock):

        self.collector.collect()

        metrics = {
            '28_A76569020000.t': 22.4375,
            '28_2F702A010000.p11': 999
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)


###############################################################################
if __name__ == "__main__":
    unittest.main()
