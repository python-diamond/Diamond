#!/usr/bin/python
# coding=utf-8
################################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from test import run_only
from mock import MagicMock
from mock import patch

from diamond.collector import Collector
from mongodb import MongoDBCollector

################################################################################


def run_only_if_pymongo_is_available(func):
    try:
        import pymongo
        pymongo  # workaround for pyflakes issue #13
    except ImportError:
        pymongo = None
    pred = lambda: pymongo is not None
    return run_only(func, pred)


class TestMongoDBCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('MongoDBCollector', {
            'host': 'localhost:27017',
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

    def _annotate_connection(self, connector_mock, data):
        connector_mock.return_value = self.connection
        self.connection.db.command.return_value = data
        self.connection.database_names.return_value = ['db1']


################################################################################
if __name__ == "__main__":
    unittest.main()
