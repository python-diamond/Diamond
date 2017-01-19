#!/usr/bin/python
# coding=utf-8
##########################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import run_only
from test import unittest
from mock import patch

from pgbouncer import PgbouncerCollector

##########################################################################


def run_only_if_psycopg2_is_available(func):
    try:
        import psycopg2
    except ImportError:
        psycopg2 = None
    pred = lambda: psycopg2 is not None
    return run_only(func, pred)


class TestPgbouncerCollector(CollectorTestCase):

    def setUp(self):
        config = get_collector_config('PgbouncerCollector', {})

        self.collector = PgbouncerCollector(config, None)

    def test_import(self):
        self.assertTrue(PgbouncerCollector)

    @run_only_if_psycopg2_is_available
    @patch.object(PgbouncerCollector, '_get_stats_by_database')
    @patch.object(PgbouncerCollector, 'publish')
    def test_default(self, publish, _get_stats_by_database):
        _get_stats_by_database.return_value = {'foo': {'bar': 42}}

        self.collector.collect()

        _get_stats_by_database.assert_called_with(
            'localhost', '6432', 'postgres', '')

        self.assertPublished(publish, 'default.foo.bar', 42)

    @run_only_if_psycopg2_is_available
    @patch.object(PgbouncerCollector, '_get_stats_by_database')
    @patch.object(PgbouncerCollector, 'publish')
    def test_instance_names(self, publish, _get_stats_by_database):
        def side_effect(host, port, user, password):
            if (host, port) == ('127.0.0.1', '6432'):
                return {'foo': {'bar': 42}}
            elif (host, port) == ('localhost', '6433'):
                return {'foo': {'baz': 24}}

        _get_stats_by_database.side_effect = side_effect

        config = get_collector_config('PgbouncerCollector', {
            'instances': {
                'alpha': {
                    'host': '127.0.0.1',
                    'port': '6432',
                },
                'beta': {
                    'host': 'localhost',
                    'port': '6433',
                },
            }
        })
        collector = PgbouncerCollector(config, None)
        collector.collect()

        self.assertPublished(publish, 'alpha.foo.bar', 42)
        self.assertPublished(publish, 'beta.foo.baz', 24)

    @run_only_if_psycopg2_is_available
    @patch.object(PgbouncerCollector, '_get_stats_by_database')
    def test_override_user_password(self, _get_stats_by_database):
        _get_stats_by_database.return_value = {}

        config = get_collector_config('PgbouncerCollector', {
            'instances': {
                'test1': {
                    'host': '127.0.0.1',
                    'port': '6433',
                    'password': 'foobar',
                },
                'test2': {
                    'host': '127.0.0.2',
                    'port': '6432',
                    'user': 'pgbouncer',
                }
            }
        })
        collector = PgbouncerCollector(config, None)
        collector.collect()

        _get_stats_by_database.assert_any_call(
            '127.0.0.1', '6433', 'postgres', 'foobar')
        _get_stats_by_database.assert_any_call(
            '127.0.0.2', '6432', 'pgbouncer', '')


##########################################################################
if __name__ == "__main__":
    unittest.main()
