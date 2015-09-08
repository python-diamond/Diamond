#!/usr/bin/python
# coding=utf-8
################################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest

from rds import RdsCollector

################################################################################


class TestRdsCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('RdsCollector', {
            'interval': 10
        })

        self.collector = RdsCollector(config, None)

    def test_import(self):
        self.assertTrue(RdsCollector)

################################################################################
if __name__ == "__main__":
    unittest.main()
