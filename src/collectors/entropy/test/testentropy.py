#!/usr/bin/python
# coding=utf-8
################################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest

from entropy import EntropyStatCollector

################################################################################


class TestEntropyStatCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('EntropyStatCollector', {
        })

        self.collector = EntropyStatCollector(config, None)

    def test_import(self):
        self.assertTrue(EntropyStatCollector)

################################################################################
if __name__ == "__main__":
    unittest.main()
