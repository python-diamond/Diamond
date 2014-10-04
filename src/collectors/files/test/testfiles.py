#!/usr/bin/python
# coding=utf-8
###############################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest

from files import FilesCollector


###############################################################################

class TestFilesCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('FilesCollector', {
        })
        self.collector = FilesCollector(config, None)

    def test_import(self):
        self.assertTrue(FilesCollector)

###############################################################################
if __name__ == "__main__":
    unittest.main()
