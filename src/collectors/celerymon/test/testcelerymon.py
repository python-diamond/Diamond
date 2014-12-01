#!/usr/bin/python
# coding=utf-8
###############################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest

from celerymon import CelerymonCollector


###############################################################################

class TestCelerymonCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('CelerymonCollector', {
        })
        self.collector = CelerymonCollector(config, None)

    def test_import(self):
        self.assertTrue(CelerymonCollector)

###############################################################################
if __name__ == "__main__":
    unittest.main()
