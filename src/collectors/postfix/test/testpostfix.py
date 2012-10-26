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
        
    @patch.object(Collector, 'publish')
    def test_should_work_with_synthetic_data(self, publish_mock):
        with patch.object(PostfixCollector,
                          'getJson',
                          Mock(return_value='{"local": {}, "clients": {"127.0.0.1": 1}, "recv": {"status": {}, "resp_codes": {}}, "send": {"status": {"sent": 0}, "resp_codes": {"2.0.0": 0}}, "in": {"status": {}, "resp_codes": {}}}')):
            self.collector.collect()
            
        self.assertPublishedMany(publish_mock, {})

        with patch.object(PostfixCollector,
                          'getJson',
                          Mock(return_value='{"local": {}, "clients": {"127.0.0.1": 2}, "recv": {"status": {}, "resp_codes": {}}, "send": {"status": {"sent": 4}, "resp_codes": {"2.0.0": 5}}, "in": {"status": {}, "resp_codes": {}}}')):
            self.collector.collect()

        self.assertPublishedMany(publish_mock, {
            'send.status.sent': 4,
            'send.resp_codes.2_0_0': 5,
            'clients.127_0_0_1': 1,
        })

################################################################################
if __name__ == "__main__":
    unittest.main()
