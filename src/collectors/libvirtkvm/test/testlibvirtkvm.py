#!/usr/bin/python
# coding=utf-8
###############################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest

from libvirtkvm import LibvirtKVMCollector


###############################################################################

class TestLibvirtKVMCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('LibvirtKVMCollector', {
        })
        self.collector = LibvirtKVMCollector(config, None)

    def test_import(self):
        self.assertTrue(LibvirtKVMCollector)

###############################################################################
if __name__ == "__main__":
    unittest.main()
