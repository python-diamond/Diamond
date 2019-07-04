#!/usr/bin/python
# coding=utf-8
###############################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest

from logstash import LogstashCollector


###############################################################################

class TestLogstashCollector(CollectorTestCase):

    def setUp(self):
        config = get_collector_config('LogstashCollector', {
        })
        self.collector = LogstashCollector(config, None)

    def test_import(self):
        self.assertTrue(LogstashCollector)

###############################################################################
if __name__ == "__main__":
    unittest.main()
