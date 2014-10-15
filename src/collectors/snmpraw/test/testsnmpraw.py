#!/usr/bin/python
# coding=utf-8
###############################################################################
import time
from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import Mock
from mock import patch

from diamond.collector import Collector
from snmpraw import SNMPRawCollector


###############################################################################

class TestSNMPRawCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('SNMPRawCollector', {
        })
        self.collector = SNMPRawCollector(config, None)

    def test_import(self):
        self.assertTrue(SNMPRawCollector)

    @patch.object(Collector, 'publish_metric')
    @patch.object(time, 'time', Mock(return_value=1000))
    @patch.object(SNMPRawCollector, '_get_value', Mock(return_value=5))
    def test_metric(self, collect_mock):
        test_config = {'devices': {'test': {'oids': {'1.1.1.1': 'test'}}}}
        self.collector.config.update(test_config)

        path = '.'.join([self.collector.config['path_prefix'], 'test',
                         self.collector.config['path_suffix'], 'test'])

        self.collector.collect_snmp('test', None, None, None)
        metric = collect_mock.call_args[0][0]

        self.assertEqual(metric.metric_type, 'GAUGE')
        self.assertEqual(metric.ttl, None)
        self.assertEqual(metric.value, self.collector._get_value())
        self.assertEqual(metric.precision, self.collector._precision(5))
        self.assertEqual(metric.host, None)
        self.assertEqual(metric.path, path)
        self.assertEqual(metric.timestamp, 1000)


###############################################################################
if __name__ == "__main__":
    unittest.main()
