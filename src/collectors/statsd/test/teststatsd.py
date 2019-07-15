#!/usr/bin/python
# coding=utf-8
###############################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest

from statsd import StatsdCollector

###############################################################################


class TestStatsdCollector(CollectorTestCase):

    def setUp(self):
        config = get_collector_config('StatsdCollector', {})
        self.collector = StatsdCollector(config, None)

    def test_import(self):
        self.assertTrue(StatsdCollector)

###############################################################################
if __name__ == "__main__":
    unittest.main()

