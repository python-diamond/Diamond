#!/usr/bin/python
# coding=utf-8
##########################################################################

import time

from test import unittest
from mock import Mock
from mock import patch
from mock import call

import configobj

from diamond.metric import Metric

from diamond import util
ElasticsearchHandler = util.load_class_from_name(
    'diamond.handler.elasticsearch.ElasticsearchHandler', 'handler_')


# These two methods are used for overriding
# the Elasticsearch python client
# Please check the Test class' setUp and tearDown methods
def fake_connect(self):
    # used for 'we can connect' tests
    self.elasticclient = Mock()
    self.elasticclient.bulk = Mock(return_value={'errors': False})


def fake_bad_connect(self):
    # used for 'we can not connect' tests
    self.elasticclient = Mock()
    self.elasticclient.bulk = Mock(return_value={'errors': True})


class TestElasticsearchHandler(unittest.TestCase):

    def setUp(self):
        self.__connect_method = ElasticsearchHandler
        ElasticsearchHandler._connect = fake_connect

    def tearDown(self):
        # restore the override
        ElasticsearchHandler._connect = self.__connect_method

    def test_single_metric(self):
        config = configobj.ConfigObj()
        config['index_rotation'] = None
        config['batch'] = 1

        metric = Metric('servers.com.example.www.cpu.total.idle',
                        0, timestamp=1234567, host='will-be-ignored')

        expected_data = [
            call(
                '{"index": {"_index": "metrics", "_type": "metric", '
                '"_id": "1234567_servers.com.example.www.cpu.total.idle"}}\n'
                '{"timestamp": 1234567000, '
                '"path": "servers.com.example.www.cpu.total.idle", "value": 0, '
                '"host": "will-be-ignored", "metric_type": "COUNTER", '
                '"raw_value": "None", "ttl": None}'
            ),
        ]

        handler = ElasticsearchHandler(config)
        handler._connect()

        handler.process(metric)

        self.assertEqual(
            handler.elasticclient.bulk.call_count, len(expected_data))
        self.assertEqual(
            handler.elasticclient.bulk.call_args_list, expected_data)

    def test_multi_no_batching(self):
        config = configobj.ConfigObj()
        config['index_rotation'] = None
        config['batch'] = 1

        metrics = [
            Metric('metricname1', 0, timestamp=123),
            Metric('metricname2', 0, timestamp=123),
        ]

        expected_data = [
            call(
                '{"index": {"_index": "metrics", "_type": "metric", '
                '"_id": "123_metricname1"}}\n'
                '{"timestamp": 123000, "path": "metricname1", "value": 0, '
                '"host": "None", "metric_type": "COUNTER", '
                '"raw_value": "None", "ttl": None}'
            ),
            call(
                '{"index": {"_index": "metrics", "_type": "metric", '
                '"_id": "123_metricname2"}}\n'
                '{"timestamp": 123000, "path": "metricname2", "value": 0, '
                '"host": "None", "metric_type": "COUNTER", '
                '"raw_value": "None", "ttl": None}'
            ),
        ]

        handler = ElasticsearchHandler(config)
        handler._connect()

        for m in metrics:
            handler.process(m)

        self.assertEqual(
            handler.elasticclient.bulk.call_count, len(expected_data))

        self.assertEqual(
            handler.elasticclient.bulk.call_args_list, expected_data)

    def test_multi_with_batching(self):
        config = configobj.ConfigObj()
        config['index_rotation'] = None
        config['batch'] = 2

        metrics = [
            Metric('metricname1', 0, timestamp=123),
            Metric('metricname2', 0, timestamp=123),
        ]

        expected_data = [
            call(
                '{"index": {"_index": "metrics", "_type": "metric", '
                '"_id": "123_metricname1"}}\n'
                '{"timestamp": 123000, "path": "metricname1", "value": 0, '
                '"host": "None", "metric_type": "COUNTER", '
                '"raw_value": "None", "ttl": None}'
                '\n'
                '{"index": {"_index": "metrics", "_type": "metric", '
                '"_id": "123_metricname2"}}\n'
                '{"timestamp": 123000, "path": "metricname2", "value": 0, '
                '"host": "None", "metric_type": "COUNTER", '
                '"raw_value": "None", "ttl": None}'
            ),
        ]

        handler = ElasticsearchHandler(config)
        handler._connect()

        for m in metrics:
            handler.process(m)

        self.assertEqual(
            handler.elasticclient.bulk.call_count, 1)

        self.assertEqual(
            handler.elasticclient.bulk.call_args_list, expected_data)

    def test_backlog(self):
        config = configobj.ConfigObj()
        config['index_rotation'] = None
        config['batch'] = 1

        # start trimming after X batchsizes in buffer
        config['max_backlog_multiplier'] = 2
        # when trimming: keep last X batchsizes
        config['trim_backlog_multiplier'] = 2

        metrics = [
            Metric('metricname1', 0, timestamp=123),
            Metric('metricname2', 0, timestamp=123),
            Metric('metricname3', 0, timestamp=123),
            Metric('metricname4', 0, timestamp=123),
            Metric('metricname5', 0, timestamp=123),
            Metric('metricname6', 0, timestamp=123),
            Metric('metricname7', 0, timestamp=123),
            Metric('metricname8', 0, timestamp=123),
        ]

        expected_data = [
            call(
                '{"index": {"_index": "metrics", "_type": "metric", '
                '"_id": "123_metricname6"}}\n'
                '{"timestamp": 123000, "path": "metricname6", "value": 0, '
                '"host": "None", "metric_type": "COUNTER", '
                '"raw_value": "None", "ttl": None}'
                '\n'
                '{"index": {"_index": "metrics", "_type": "metric", '
                '"_id": "123_metricname7"}}\n'
                '{"timestamp": 123000, "path": "metricname7", "value": 0, '
                '"host": "None", "metric_type": "COUNTER", '
                '"raw_value": "None", "ttl": None}'
                '\n'
                '{"index": {"_index": "metrics", "_type": "metric", '
                '"_id": "123_metricname8"}}\n'
                '{"timestamp": 123000, "path": "metricname8", "value": 0, '
                '"host": "None", "metric_type": "COUNTER", '
                '"raw_value": "None", "ttl": None}'
            ),
        ]

        # simulate an unreachable Elasticsearch host
        # thus force backlog functionality
        ElasticsearchHandler._connect = fake_bad_connect
        handler = ElasticsearchHandler(config)
        handler._connect()

        for m in metrics:
            handler.process(m)

        self.assertEqual(
            handler.elasticclient.bulk.call_count, 8)

        # Check last call with expected_data
        self.assertEqual(
            [handler.elasticclient.bulk.call_args_list[-1]], expected_data)

    def test_error_throttling(self):
        """
        This is more of a generic test checking that the _throttle_error method
        works as expected

        TODO: test that the ElasticsearchHandler calls _throttle_error
        in the right circumstances.
        """
        config = configobj.ConfigObj()
        config['server_error_interval'] = '0.1'

        handler = ElasticsearchHandler(config)

        debug_mock = Mock()
        patch_debug = patch.object(handler.log, 'debug', debug_mock)
        error_mock = Mock()
        patch_error = patch.object(handler.log, 'error', error_mock)

        patch_debug.start()
        patch_error.start()

        calls = 5
        for _ in range(calls):
            handler._throttle_error('Error Message')

        # .error should have been called only once
        self.assertEqual(error_mock.call_count, 1)
        self.assertEqual(debug_mock.call_count, calls - 1)

        handler._reset_errors()

        debug_mock.reset_mock()
        error_mock.reset_mock()

        for _ in range(calls):
            handler._throttle_error('Error Message')
            time.sleep(0.065)

        # error should have been called 0.065 * 5 / 0.1 = 3 times
        self.assertEqual(error_mock.call_count, 3)
        self.assertEqual(debug_mock.call_count, 2)
        patch_debug.stop()
        patch_error.stop()

if __name__ == "__main__":
    unittest.main()
