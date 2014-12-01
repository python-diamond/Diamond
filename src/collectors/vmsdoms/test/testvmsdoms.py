#!/usr/bin/python
# coding=utf-8
###############################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest

from vmsdoms import VMSDomsCollector


###############################################################################

class TestVMSDomsCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('VMSDomsCollector', {
        })
        self.collector = VMSDomsCollector(config, None)

    def test_import(self):
        self.assertTrue(VMSDomsCollector)

###############################################################################
if __name__ == "__main__":
    unittest.main()
