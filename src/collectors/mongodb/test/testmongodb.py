#!/usr/bin/python
# coding=utf-8
################################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from test import run_only
from mock import MagicMock
from mock import patch
from mock import call

from diamond.collector import Collector
from mongodb import MongoDBCollector

################################################################################


def run_only_if_pymongo_is_available(func):
    try:
        import pymongo
    except ImportError:
        pymongo = None
    pred = lambda: pymongo is not None
    return run_only(func, pred)


class TestMongoDBCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('MongoDBCollector', {
            'host': 'localhost:27017',
            'databases': '^db',
        })
        self.collector = MongoDBCollector(config, None)
        self.connection = MagicMock()

    def test_import(self):
        self.assertTrue(MongoDBCollector)

    @run_only_if_pymongo_is_available
    @patch('pymongo.Connection')
    @patch.object(Collector, 'publish')
    def test_should_publish_nested_keys_for_server_stats(self,
                                                         publish_mock,
                                                         connector_mock):
        data = {'more_keys': {'nested_key': 1}, 'key': 2, 'string': 'str'}
        self._annotate_connection(connector_mock, data)

        self.collector.collect()

        self.connection.db.command.assert_called_once_with('serverStatus')
        self.assertPublishedMany(publish_mock, {
            'more_keys.nested_key': 1,
            'key': 2
        })

    @run_only_if_pymongo_is_available
    @patch('pymongo.Connection')
    @patch.object(Collector, 'publish')
    def test_should_publish_nested_keys_for_db_stats(self,
                                                     publish_mock,
                                                     connector_mock):
        data = {'db_keys': {'db_nested_key': 1}, 'dbkey': 2, 'dbstring': 'str'}
        self._annotate_connection(connector_mock, data)

        self.collector.collect()

        self.connection['db1'].command.assert_called_once_with('dbStats')
        metrics = {
            'db_keys.db_nested_key': 1,
            'dbkey': 2
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

    @run_only_if_pymongo_is_available
    @patch('pymongo.Connection')
    @patch.object(Collector, 'publish')
    def test_should_publish_stats_with_long_type(self,
                                                 publish_mock,
                                                 connector_mock):
        data = {'more_keys': long(1), 'key': 2, 'string': 'str'}
        self._annotate_connection(connector_mock, data)

        self.collector.collect()

        self.connection.db.command.assert_called_once_with('serverStatus')
        self.assertPublishedMany(publish_mock, {
            'more_keys': 1,
            'key': 2
        })

    @run_only_if_pymongo_is_available
    @patch('pymongo.Connection')
    @patch.object(Collector, 'publish')
    def test_should_ignore_unneeded_databases(self,
                                              publish_mock,
                                              connector_mock):
        self._annotate_connection(connector_mock, {})

        self.collector.collect()

        assert call('baddb') not in self.connection.__getitem__.call_args_list

    @run_only_if_pymongo_is_available
    @patch('pymongo.Connection')
    @patch.object(Collector, 'publish')
    def test_should_ignore_unneeded_collections(self,
                                                publish_mock,
                                                connector_mock):
        data = {'more_keys': long(1), 'key': 2, 'string': 'str'}
        self._annotate_connection(connector_mock, data)

        self.connection['db1'].collection_names.return_value = ['collection1',
                                                                'tmp.mr.tmp1']
        self.connection['db1'].command.return_value = {'key': 2,
                                                       'string': 'str'}

        self.collector.collect()

        self.connection.db.command.assert_called_once_with('serverStatus')
        self.connection['db1'].collection_names.assert_called_once_with()
        self.connection['db1'].command.assert_any_call('dbStats')
        self.connection['db1'].command.assert_any_call('collstats',
                                                       'collection1')
        assert call('collstats', 'tmp.mr.tmp1') not in self.connection['db1'].command.call_args_list  # NOQA
        metrics = {
            'databases.db1.collection1.key': 2,
        }

        self.assertPublishedMany(publish_mock, metrics)

    def _annotate_connection(self, connector_mock, data):
        connector_mock.return_value = self.connection
        self.connection.db.command.return_value = data
        self.connection.database_names.return_value = ['db1', 'baddb']


class TestMongoMultiHostDBCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('MongoDBCollector', {
            'hosts': ['localhost:27017', 'localhost:27057'],
            'databases': '^db',
        })
        self.collector = MongoDBCollector(config, None)
        self.connection = MagicMock()

    def test_import(self):
        self.assertTrue(MongoDBCollector)

    @run_only_if_pymongo_is_available
    @patch('pymongo.Connection')
    @patch.object(Collector, 'publish')
    def test_should_publish_nested_keys_for_server_stats(self,
                                                         publish_mock,
                                                         connector_mock):
        data = {'more_keys': {'nested_key': 1}, 'key': 2, 'string': 'str'}
        self._annotate_connection(connector_mock, data)

        self.collector.collect()

        self.connection.db.command.assert_called_with('serverStatus')
        self.assertPublishedMany(publish_mock, {
            'localhost_27017.more_keys.nested_key': 1,
            'localhost_27057.more_keys.nested_key': 1,
            'localhost_27017.key': 2,
            'localhost_27057.key': 2
        })

    @run_only_if_pymongo_is_available
    @patch('pymongo.Connection')
    @patch.object(Collector, 'publish')
    def test_should_publish_nested_keys_for_db_stats(self,
                                                     publish_mock,
                                                     connector_mock):
        data = {'db_keys': {'db_nested_key': 1}, 'dbkey': 2, 'dbstring': 'str'}
        self._annotate_connection(connector_mock, data)

        self.collector.collect()

        self.connection['db1'].command.assert_called_with('dbStats')
        metrics = {
            'localhost_27017.db_keys.db_nested_key': 1,
            'localhost_27057.db_keys.db_nested_key': 1,
            'localhost_27017.dbkey': 2,
            'localhost_27057.dbkey': 2
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

    @run_only_if_pymongo_is_available
    @patch('pymongo.Connection')
    @patch.object(Collector, 'publish')
    def test_should_publish_stats_with_long_type(self,
                                                 publish_mock,
                                                 connector_mock):
        data = {'more_keys': long(1), 'key': 2, 'string': 'str'}
        self._annotate_connection(connector_mock, data)

        self.collector.collect()

        self.connection.db.command.assert_called_with('serverStatus')
        self.assertPublishedMany(publish_mock, {
            'localhost_27017.more_keys': 1,
            'localhost_27057.more_keys': 1,
            'localhost_27017.key': 2,
            'localhost_27057.key': 2
        })

    @run_only_if_pymongo_is_available
    @patch('pymongo.Connection')
    @patch.object(Collector, 'publish')
    def test_should_ignore_unneeded_databases(self,
                                              publish_mock,
                                              connector_mock):
        self._annotate_connection(connector_mock, {})

        self.collector.collect()

        assert call('baddb') not in self.connection.__getitem__.call_args_list

    @run_only_if_pymongo_is_available
    @patch('pymongo.Connection')
    @patch.object(Collector, 'publish')
    def test_should_ignore_unneeded_collections(self,
                                                publish_mock,
                                                connector_mock):
        data = {'more_keys': long(1), 'key': 2, 'string': 'str'}
        self._annotate_connection(connector_mock, data)

        self.connection['db1'].collection_names.return_value = ['collection1',
                                                                'tmp.mr.tmp1']
        self.connection['db1'].command.return_value = {'key': 2,
                                                       'string': 'str'}

        self.collector.collect()

        self.connection.db.command.assert_called_with('serverStatus')
        self.connection['db1'].collection_names.assert_called_with()
        self.connection['db1'].command.assert_any_call('dbStats')
        self.connection['db1'].command.assert_any_call('collstats',
                                                       'collection1')
        assert call('collstats', 'tmp.mr.tmp1') not in self.connection['db1'].command.call_args_list  # NOQA
        metrics = {
            'localhost_27017.databases.db1.collection1.key': 2,
            'localhost_27057.databases.db1.collection1.key': 2,
        }

        self.assertPublishedMany(publish_mock, metrics)

    def _annotate_connection(self, connector_mock, data):
        connector_mock.return_value = self.connection
        self.connection.db.command.return_value = data
        self.connection.database_names.return_value = ['db1', 'baddb']


################################################################################
if __name__ == "__main__":
    unittest.main()
