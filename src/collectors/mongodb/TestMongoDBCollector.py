#!/usr/bin/python
################################################################################

from test import *

from diamond.collector import Collector
from mongodb import MongoDBCollector

################################################################################

class TestMongoDBCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('MongoDBCollector', {
            'host'  : 'localhost:27017',
        })
        self.collector = MongoDBCollector(config, None)

    @patch('pymongo.Connection')
    @patch.object(Collector, 'publish')
    def test_should_publish_nested_keys(self, publish_mock, connector_mock):
        connection = Mock()
        data = {'more_keys': {'nested_key': 1}, 'key': 2, 'string': 'str'}
        connector_mock.return_value = connection
        connection.db.command.return_value = data

        self.collector.collect()

        connection.db.command.assert_called_once_with('serverStatus')
        self.assertPublishedMany(publish_mock, {
            'more_keys.nested_key': 1,
            'key' : 2
        })

################################################################################
if __name__ == "__main__":
    unittest.main()
