#!/usr/bin/python
# coding=utf-8
##########################################################################
import os
import json
from test import CollectorTestCase
from test import get_collector_config
from test import unittest

from diamond.collector import Collector
from fluentd import FluentdCollector


dirname = os.path.dirname(__file__)
fixtures_path = os.path.join(dirname, 'fixtures/')


class TestFluentdCollector(CollectorTestCase):

    def setUp(self):
        config = get_collector_config('FluentdCollector', {
            'interval': 10,
            'collect': {
                'kinesis': [
                    'buffer_queue_length',
                    'buffer_total_queued_size',
                    'retry_count'
                    ]
                }
        })

        self.collector = FluentdCollector(config, None)

    def test_import(self):
        self.assertTrue(FluentdCollector)

    def test_api_output_parse(self):
        f = open(os.path.join(fixtures_path, "example.stat")).read()
        stat = json.loads(f)
        self.assertTrue(len(self.collector.parse_api_output(stat)) is 3)

    def test_api_output_parse_empty(self):
        f = open(os.path.join(fixtures_path, "example_empty.stat")).read()
        stat = json.loads(f)
        self.assertTrue(len(self.collector.parse_api_output(stat)) is 0)

if __name__ == "__main__":
    unittest.main()
