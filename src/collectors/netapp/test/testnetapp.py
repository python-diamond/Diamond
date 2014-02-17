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
from netapp import NetAppCollector


###############################################################################

class TestNetAppCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('NetAppCollector', {
        })
        self.collector = NetAppCollector(config, None)

    def test_import(self):
        self.assertTrue(NetAppCollector)

###############################################################################
if __name__ == "__main__":
    unittest.main()
