#!/usr/bin/python
# coding=utf-8
###############################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest

from netapp_inode import netapp_inode


###############################################################################

class Testnetapp_inode(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('netapp_inode', {
        })
        self.collector = netapp_inode(config, None)

    def test_import(self):
        self.assertTrue(netapp_inode)

###############################################################################
if __name__ == "__main__":
    unittest.main()
