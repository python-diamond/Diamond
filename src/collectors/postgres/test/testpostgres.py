#!/usr/bin/python
# coding=utf-8
##########################################################################

from test import CollectorTestCase
from test import get_collector_config

from mock import patch, Mock
from postgres import PostgresqlCollector


class TestPostgresqlCollector(CollectorTestCase):

    def setUp(self, allowed_names=None):
        if not allowed_names:
            allowed_names = []

        default_config = get_collector_config('PostgresqlCollector', {})
        self.default_collector = PostgresqlCollector(default_config, None)

        config = get_collector_config('PostgresqlCollector', {
            'password': 'default_password',
            'port': 5432,
            'instances': {
                'postgres_a': {
                    'host': 'db1.loc',
                    'password_provider': 'pgpass',
                },
                'postgres_b': {
                    'host': 'db2.loc',
                    'port': 5433,
                    'password': 'instance_password_b',
                }
            }
        })
        self.collector = PostgresqlCollector(config, None)

    def test_import(self):
        self.assertTrue(PostgresqlCollector)

    def test_config_with_empty_instance(self):
        result = self.default_collector.collect()
        self.assertEqual(result, {})

    def test_config_override(self):
        self.assertEqual(self.collector._get_config('postgres_a', 'port'), 5432)

        self.assertEqual(self.collector._get_config('postgres_b', 'port'), 5433)

    @patch('postgres.psycopg2')
    def test_connect_with_password(self, psycopg2_mock):
        conn_mock = Mock()
        psycopg2_mock.connect.return_value = conn_mock

        ret = self.collector._connect('postgres_b', 'test_db')

        self.assertTrue(conn_mock.set_isolation_level.called)
        self.assertEqual(ret, conn_mock)
        psycopg2_mock.connect.assert_called_once_with(
            database='test_db', host='db2.loc', password='instance_password_b',
            port=5433, sslmode='disable', user='postgres'
        )

    @patch('postgres.psycopg2')
    def test_connect_with_pgpass(self, psycopg2_mock):
        conn_mock = Mock()
        psycopg2_mock.connect.return_value = conn_mock

        ret = self.collector._connect('postgres_a', 'test_db')

        self.assertTrue(conn_mock.set_isolation_level.called)
        self.assertEqual(ret, conn_mock)
        psycopg2_mock.connect.assert_called_once_with(
            database='test_db', host='db1.loc',
            port=5432, sslmode='disable', user='postgres'
        )

    @patch('postgres.psycopg2')
    def test_connect_error(self, psycopg2_mock):
        psycopg2_mock.connect.side_effect = Exception('Some db exc')

        with self.assertRaises(Exception):
            self.collector._connect('test_db')
