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
