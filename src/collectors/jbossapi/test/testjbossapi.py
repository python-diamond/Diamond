#!/usr/bin/python
# coding=utf-8
###############################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from test import run_only
from mock import Mock
from mock import patch

from diamond.collector import Collector
from jbossapi import JbossApiCollector


###############################################################################

class TestJbossApiCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('JbossApiCollector', {
        })
        self.collector = JbossApiCollector(config, None)

    def test_import(self):
        self.assertTrue(JbossApiCollector)

###############################################################################
if __name__ == "__main__":
    unittest.main()
