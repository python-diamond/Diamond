#!/usr/bin/python
# coding=utf-8
###############################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import run_only
from mock import patch

from slony import SlonyCollector


def run_only_if_psycopg2_is_available(func):
    try:
        import psycopg2
    except ImportError:
        psycopg2 = None
    pred = lambda: psycopg2 is not None
    return run_only(func, pred)


class TestSlonyCollector(CollectorTestCase):

    def setUp(self):
        config = get_collector_config('SlonyCollector', {})
        self.collector = SlonyCollector(config, None)

    def test_import(self):
        self.assertTrue(SlonyCollector)

    @run_only_if_psycopg2_is_available
    @patch.object(SlonyCollector, '_get_stats_by_database')
    @patch.object(SlonyCollector, 'publish')
    def test_default(self, publish, _get_stats_by_database):
        _get_stats_by_database.return_value = [('foo', 7)]

        self.collector.collect()
        _get_stats_by_database.assert_called_with(
            'localhost',
            5432,
            'postgres',
            'postgres',
            'postgres',
            '_postgres',
            'Node [0-9]+ - postgres@localhost',

        )

        self.assertPublished(publish, 'foo', 7)

    @run_only_if_psycopg2_is_available
    @patch.object(SlonyCollector, '_get_stats_by_database')
    @patch.object(SlonyCollector, 'publish')
    def test_instances(self, publish, _get_stats_by_database):
        def side_effect(host, port, user, pwd, slony_db, slony_schema, node):
            if (slony_db, slony_schema) == ('postgres', '_postgres'):
                return [('foo', 7)]
            elif (slony_db, slony_schema) == ('data', '_data'):
                return [('bar', 14)]

        _get_stats_by_database.side_effect = side_effect

        config = get_collector_config('SlonyCollector', {
            'instances': {
                'alpha': {
                    'slony_db': 'postgres',
                    'slony_schema': '_postgres',
                },
                'beta': {
                    'slony_db': 'data',
                    'slony_schema': '_data',
                },
            }
        })

        collector = SlonyCollector(config, None)
        collector.collect()

        self.assertPublished(publish, 'foo', 7)
        self.assertPublished(publish, 'bar', 14)

    @run_only_if_psycopg2_is_available
    @patch.object(SlonyCollector, '_get_stats_by_database')
    def test_override_user_password_nodestr(self, _get_stats_by_database):
        config = get_collector_config('SlonyCollector', {
            'instances': {
                'alpha': {
                    'slony_db': 'postgres',
                    'slony_schema': '_postgres',
                    'user': 'postgres',
                    'password': 'postgres',
                    'slony_node_string': '(.*)',
                },
                'beta': {
                    'slony_db': 'data',
                    'slony_schema': '_data',
                    'user': 'data',
                    'password': 'data',
                    'slony_node_string': 'Node (.*)',
                },
            }
        })

        collector = SlonyCollector(config, None)
        collector.collect()

        _get_stats_by_database.assert_any_call(
            'localhost', 5432, 'postgres', 'postgres',
            'postgres', '_postgres', '(.*)'
        )
        _get_stats_by_database.assert_any_call(
            'localhost', 5432, 'data', 'data',
            'data', '_data', 'Node (.*)'
        )
