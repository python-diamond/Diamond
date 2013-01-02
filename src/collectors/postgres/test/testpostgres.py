#!/usr/bin/python
# coding=utf-8
################################################################################

from test import CollectorTestCase
from test import get_collector_config

from postgres import PostgresqlCollector


class TestPostgresqlCollector(CollectorTestCase):
    def setUp(self, allowed_names=None):
        if not allowed_names:
            allowed_names = []
        config = get_collector_config('PostgresqlCollector', {
        })
        self.collector = PostgresqlCollector(config, None)

    def test_import(self):
        self.assertTrue(PostgresqlCollector)
