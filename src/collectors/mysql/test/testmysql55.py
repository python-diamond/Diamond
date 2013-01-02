#!/usr/bin/python
# coding=utf-8
################################################################################

from test import CollectorTestCase
from test import get_collector_config

from mysql55 import MySQLPerfCollector


class TestMySQLPerfCollector(CollectorTestCase):
    def setUp(self, allowed_names=None):
        if not allowed_names:
            allowed_names = []
        config = get_collector_config('MySQLPerfCollector', {
            'allowed_names': allowed_names,
            'interval': 1
        })
        self.collector = MySQLPerfCollector(config, None)

    def test_import(self):
        self.assertTrue(MySQLPerfCollector)
