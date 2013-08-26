#!/usr/bin/python
# coding=utf-8
################################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import Mock
from mock import patch

from diamond.collector import Collector
from supervisord import SupervisordCollector

################################################################################


class TestSupervisordCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('SupervisordCollector', {})
        self.collector = SupervisordCollector(config, None)
        self.assertTrue(self.collector)

    def test_import(self):
        self.assertTrue(SupervisordCollector)

    @patch.object(Collector, 'publish')
    def test_success(self, publish_mock):

        self.collector.getAllProcessInfo = Mock(
            return_value=eval(self.getFixture('valid_fixture').getvalue()))

        self.collector.collect()

        metrics = {
            'test_group.test_name_1.state': 20,
            'test_group.test_name_1.uptime':  5,
            'test_group.test_name_2.state': 200,
            'test_group.test_name_2.uptime': 500
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

################################################################################
if __name__ == "__main__":
    unittest.main()
