#!/usr/bin/python
# coding=utf-8
################################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest

from redshift import RedshiftCollector

################################################################################


class TestRedshiftCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('RedshiftCollector', {
            'interval': 10
        })

        self.collector = RedshiftCollector(config, None)

    def test_import(self):
        self.assertTrue(RedshiftCollector)

################################################################################
if __name__ == "__main__":
    unittest.main()
