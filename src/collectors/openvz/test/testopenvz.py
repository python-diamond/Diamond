#!/usr/bin/python
# coding=utf-8
###############################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from test import Mock
from test import patch

from diamond.collector import Collector

from openvz import OpenvzCollector

###############################################################################


class TestOpenvzCollector(CollectorTestCase):

    def setUp(self):
        config = get_collector_config('OpenvzCollector', {})

        self.collector = OpenvzCollector(config, None)

    def test_import(self):
        self.assertTrue(OpenvzCollector)

    @patch.object(Collector, 'publish')
    def test_parse_values(self, publish_mock):
        collector_mock = patch.object(OpenvzCollector, 'poll', Mock(
            return_value=self.getFixture('vzlist.json').getvalue()))
        collector_mock.start()
        self.collector.collect()
        collector_mock.stop()

        metrics = {
            # DNS
            'dns_home_loc.kmemsize.held': 5151725,
            'dns_home_loc.uptime': 1316250.125,
            'dns_home_loc.laverage.01': 0.01,
            'dns_home_loc.laverage.05': 0.05,
            'dns_home_loc.laverage.15': 0.15,
            # MQTT
            'mqtt_home_loc.kmemsize.held': 4930969,
            'mqtt_home_loc.uptime': 126481.188,
            'mqtt_home_loc.laverage.01': 0.1,
            'mqtt_home_loc.laverage.05': 0.5,
            'mqtt_home_loc.laverage.15': 1.5,
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

###############################################################################
if __name__ == "__main__":
    unittest.main()
