#!/usr/bin/python
# coding=utf-8
################################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import Mock
from mock import patch

from diamond.collector import Collector
from postfix import PostfixCollector

################################################################################


class TestPostfixCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('PostfixCollector', {
            'host':     'localhost',
            'port':     7777,
            'interval': '1',
        })

        self.collector = PostfixCollector(config, None)

    def test_import(self):
        self.assertTrue(PostfixCollector)

    @patch.object(Collector, 'publish')
    def test_should_work_with_synthetic_data(self, publish_mock):
        first_resp = self.getFixture('postfix-stats.1.json').getvalue()
        patch_collector = patch.object(PostfixCollector,
                                        'get_json',
                                        Mock(return_value=first_resp))

        patch_collector.start()
        self.collector.collect()
        patch_collector.stop()

        self.assertPublishedMany(publish_mock, {})

        second_resp = self.getFixture('postfix-stats.2.json').getvalue()
        patch_collector = patch.object(PostfixCollector,
                                       'get_json',
                                       Mock(return_value=second_resp))

        patch_collector.start()
        self.collector.collect()
        patch_collector.stop()

        metrics = {
            'send.status.sent': 4,
            'send.resp_codes.2_0_0': 5,
            'clients.127_0_0_1': 1,
        }

        self.assertPublishedMany(publish_mock, metrics)

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])

################################################################################
if __name__ == "__main__":
    unittest.main()
