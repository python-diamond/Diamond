#!/usr/bin/python
# coding=utf-8
################################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest

from passenger_stats import PassengerCollector

################################################################################


class TestPassengerCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('PassengerCollector', {})
        self.collector = PassengerCollector(config, None)

    def test_import(self):
        self.assertTrue(PassengerCollector)

################################################################################
if __name__ == "__main__":
    unittest.main()
