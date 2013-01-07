#!/usr/bin/python
# coding=utf-8
################################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import Mock
from mock import patch

from diamond.collector import Collector
from puppetdashboard import PuppetDashboardCollector

################################################################################


class TestPuppetDashboardCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('PuppetDashboardCollector', {
            'interval': 10
        })

        self.collector = PuppetDashboardCollector(config, None)

    def test_import(self):
        self.assertTrue(PuppetDashboardCollector)

################################################################################
if __name__ == "__main__":
    unittest.main()
