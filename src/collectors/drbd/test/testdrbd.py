#!/usr/bin/python
# coding=utf-8
################################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest

from drbd import DRBDCollector

################################################################################


class TestDRBDCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('DRBDCollector', {})

        self.collector = DRBDCollector(config, None)

    def test_import(self):
        self.assertTrue(DRBDCollector)

################################################################################
if __name__ == "__main__":
    unittest.main()
