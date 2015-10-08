#!/usr/bin/python
# coding=utf-8
##########################################################################

import mock

from test import CollectorTestCase
from test import get_collector_config

from mock import patch, Mock
from postgres import PostgresqlCollector, QueryStats


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

    def _test_fetch(self, datname, cols, rows, expected_data):
        magic_rows = list()

        for row in rows:
            magic_row = mock.MagicMock()
            kv_list = zip(cols, row)

            # In [7]: type(row)
            # Out[7]: psycopg2.extras.DictRow
            # In [8]: list(row.iteritems())
            # Out[8]: [('a', 1), ('b', 2)]
            # In [9]: list(row)
            # Out[9]: [1, 2]
            magic_row.__len__.return_value = len(row)
            magic_row.__iter__.return_value = row
            magic_row.items.return_value = kv_list
            magic_row.iteritems.return_value = kv_list
            magic_row.__getitem__ = lambda _self, x, row=row: row[x]
            magic_row.get = lambda _self, x, d=None, kv_list=kv_list: dict(kv_list).get(x, d)

            magic_rows.append(magic_row)

        magic_cursor = mock.MagicMock()
        magic_cursor.execute.return_value = None
        magic_cursor.fetchall.return_value = magic_rows
        magic_cursor.description.__iter__.return_value = [(c,) for c in cols]
        magic_cursor.close.return_value = None

        magic_conn = mock.MagicMock()
        magic_conn.cursor.return_value = magic_cursor

        qs = QueryStats(dbname=datname, conn=magic_conn)
        qs.fetch('9.2')

        self.assertEqual(qs.data, expected_data)

    def test_fetch_single_simple_metric(self):
        datname = 'postgres'

        cols = ('state', 'count')

        rows = [ ('idle',    0)
               , ('running', 1)
               , ('idle',    2)
               , ('running', 3)
        ]

        expected_data = [ dict(datname=datname, metric='idle',    value=0)
                        , dict(datname=datname, metric='running', value=1)
                        , dict(datname=datname, metric='idle',    value=2)
                        , dict(datname=datname, metric='running', value=3)
        ]

        self._test_fetch(datname, cols, rows, expected_data)

    def test_fetch_single_detailed_metric(self):
        datname = 'postgres'

        cols = ['datname', 'schemaname', 'state', 'count']

        rows = [ ('wordpress', 'public', 'idle',    0)
               , ('wordpress', 'public', 'running', 1)
               , ('gitlab',    'public', 'idle',    2)
               , ('gitlab',    'public', 'running', 3)
        ]

        expected_data = [ dict(datname='wordpress', schemaname='public', metric='idle',    value=0)
                        , dict(datname='wordpress', schemaname='public', metric='running', value=1)
                        , dict(datname='gitlab',    schemaname='public', metric='idle',    value=2)
                        , dict(datname='gitlab',    schemaname='public', metric='running', value=3)
        ]

        self._test_fetch(datname, cols, rows, expected_data)

    def test_fetch_several_metrics(self):
        datname = 'postgres'

        cols = ['datname', 'schemaname', 'metric1', 'metric2', 'metric3']

        rows = [ ('wordpress', 'public', 1,    2,    3)
               , ('wordpress', 'johnny', 10,   20,   30)
               , ('gitlab',    'public', 100,  200,  300)
               , ('gitlab',    'johnny', 1000, 2000, 3000)
        ]

        expected_data = [ dict(datname='wordpress', schemaname='public', metric='metric1', value=1)
                        , dict(datname='wordpress', schemaname='public', metric='metric2', value=2)
                        , dict(datname='wordpress', schemaname='public', metric='metric3', value=3)
                        , dict(datname='wordpress', schemaname='johnny', metric='metric1', value=10)
                        , dict(datname='wordpress', schemaname='johnny', metric='metric2', value=20)
                        , dict(datname='wordpress', schemaname='johnny', metric='metric3', value=30)
                        , dict(datname='gitlab',    schemaname='public', metric='metric1', value=100)
                        , dict(datname='gitlab',    schemaname='public', metric='metric2', value=200)
                        , dict(datname='gitlab',    schemaname='public', metric='metric3', value=300)
                        , dict(datname='gitlab',    schemaname='johnny', metric='metric1', value=1000)
                        , dict(datname='gitlab',    schemaname='johnny', metric='metric2', value=2000)
                        , dict(datname='gitlab',    schemaname='johnny', metric='metric3', value=3000)
        ]

        self._test_fetch(datname, cols, rows, expected_data)
