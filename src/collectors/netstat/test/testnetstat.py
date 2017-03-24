#!/usr/bin/python
# coding=utf-8
################################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from test import patch

from diamond.collector import Collector
from netstat import NetstatCollector

################################################################################


class TestNetstatCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('NetstatCollector', {
        })

        self.collector = NetstatCollector(config, None)

    @patch.object(Collector, 'publish')
    def test(self, publish_mock):
        NetstatCollector.PROC_TCP = self.getFixturePath('proc_net_tcp')
        self.collector.collect()

        metrics = {
            'LISTEN':  9
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        print(publish_mock)
        self.assertPublishedMany(publish_mock, metrics)

################################################################################
if __name__ == "__main__":
    unittest.main()
