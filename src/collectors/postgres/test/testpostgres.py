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
        config = get_collector_config('PostgresqlCollector', {
        })
        self.collector = PostgresqlCollector(config, None)

    def test_import(self):
        self.assertTrue(PostgresqlCollector)

    @patch('postgres.psycopg2')
    def test_connect_with_password(self, psycopg2_mock):
        conn_mock = Mock()
        psycopg2_mock.connect.return_value = conn_mock

        ret = self.collector._connect('test_db')

        self.assertTrue(conn_mock.set_isolation_level.called)
        self.assertEqual(ret, conn_mock)
        psycopg2_mock.connect.assert_called_once_with(
            database='test_db', host='localhost', password='postgres',
            port=5432, sslmode='disable', user='postgres'
        )

    @patch('postgres.psycopg2')
    def test_connect_with_pgpass(self, psycopg2_mock):
        config = get_collector_config('PostgresqlCollector', {
            'password_provider': 'pgpass'
        })
        self.collector = PostgresqlCollector(config, None)

        conn_mock = Mock()
        psycopg2_mock.connect.return_value = conn_mock

        ret = self.collector._connect('test_db')

        self.assertTrue(conn_mock.set_isolation_level.called)
        self.assertEqual(ret, conn_mock)
        psycopg2_mock.connect.assert_called_once_with(
            database='test_db', host='localhost',
            port=5432, sslmode='disable', user='postgres'
        )

    @patch('postgres.psycopg2')
    def test_connect_error(self, psycopg2_mock):
        psycopg2_mock.connect.side_effect = Exception('Some db exc')

        with self.assertRaises(Exception):
            self.collector._connect('test_db')
