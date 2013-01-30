#!/usr/bin/python
# coding=utf-8
################################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest

from puppetdb import PuppetDBCollector

################################################################################


class TestPuppetDashboardCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('PuppetDBCollector', {
            'interval': 10
        })

        self.collector = PuppetDBCollector(config, None)

    def test_import(self):
        self.assertTrue(PuppetDBCollector)

################################################################################
if __name__ == "__main__":
    unittest.main()
