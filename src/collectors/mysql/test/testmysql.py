#!/usr/bin/python
# coding=utf-8
################################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import Mock
from mock import patch

from diamond.collector import Collector
from mysql import MySQLCollector

################################################################################


class TestMySQLCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('MySQLCollector', {
            'slave':    'True',
            'master':   'True',
            'innodb':   'True',
            'hosts': ['root:@localhost:3306/mysql'],
            'interval': '1',
        })

        self.collector = MySQLCollector(config, None)

    @patch.object(MySQLCollector, 'connect', Mock(return_value=True))
    @patch.object(MySQLCollector, 'disconnect', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_real_data(self, publish_mock):

        with patch.object(MySQLCollector,
                          'get_db_global_status',
                          Mock(return_value=self.getPickledResults(
                               'mysql_get_db_global_status_1.pkl'))):
            with patch.object(MySQLCollector,
                              'get_db_master_status',
                              Mock(return_value=self.getPickledResults(
                                   'get_db_master_status_1.pkl'))):
                with patch.object(MySQLCollector,
                                  'get_db_slave_status',
                                  Mock(return_value=self.getPickledResults(
                                       'get_db_slave_status_1.pkl'))):
                    with patch.object(MySQLCollector,
                                      'get_db_innodb_status',
                                      Mock(return_value=[{}])):
                        self.collector.collect()

        self.assertPublishedMany(publish_mock, {})

        with patch.object(MySQLCollector,
                          'get_db_global_status',
                          Mock(return_value=self.getPickledResults(
                               'mysql_get_db_global_status_2.pkl'))):
            with patch.object(MySQLCollector,
                              'get_db_master_status',
                              Mock(return_value=self.getPickledResults(
                                   'get_db_master_status_2.pkl'))):
                with patch.object(MySQLCollector,
                                  'get_db_slave_status',
                                  Mock(return_value=self.getPickledResults(
                                      'get_db_slave_status_2.pkl'))):
                    with patch.object(MySQLCollector,
                                      'get_db_innodb_status',
                                      Mock(return_value=[{}])):
                        self.collector.collect()

        metrics = {}
        metrics.update(self.getPickledResults(
            'mysql_get_db_global_status_expected.pkl'))
        metrics.update(self.getPickledResults(
            'get_db_master_status_expected.pkl'))
        metrics.update(self.getPickledResults(
            'get_db_slave_status_expected.pkl'))

        self.assertPublishedMany(publish_mock, metrics)

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])

################################################################################
if __name__ == "__main__":
    unittest.main()
