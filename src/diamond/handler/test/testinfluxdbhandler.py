#!/usr/bin/python
# coding=utf-8
##########################################################################

import configobj

from test import unittest, run_only

from mock import Mock, patch

from diamond.handler.influxdbHandler import InfluxdbHandler
from diamond.metric import Metric


def run_only_if_influxdb_is_available(func):
    try:
        import influxdb
    except ImportError:
        influxdb = None
    pred = lambda: influxdb is not None
    return run_only(func, pred)


class TestInfluxdbHandler(unittest.TestCase):
    @run_only_if_influxdb_is_available
    def test_single_metric_process_v_0_9(self):
        config = configobj.ConfigObj()
        config['batch_size'] = 1

        metric = Metric('servers.com.example.www.cpu.total.idle',
                        0, timestamp=1234567, host='com.example.www')

        handler = InfluxdbHandler(config)
        handler.time_multiplier = float('-inf')

        request_mock = Mock()
        patch_request = patch.object(handler.influx, 'request', request_mock)
        patch_request.start()
        handler.process(metric)
        patch_request.stop()

        expected_result = \
            'cpu,host=com.example.www total.idle=0.0 1234567\n'

        self.assertEqual(request_mock.call_count, 1)
        self.assertEqual(request_mock.call_args[1]['data'], expected_result)

    @run_only_if_influxdb_is_available
    def test_multiple_metric_process_v_0_9(self):
        config = configobj.ConfigObj()
        num = 3
        config['batch_size'] = num

        handler = InfluxdbHandler(config)
        handler.time_multiplier = float('-inf')

        request_mock = Mock()
        patch_request = patch.object(handler.influx, 'request', request_mock)
        patch_request.start()
        for i in range(num):
            metric = Metric('servers.com.example.www.cpu.total.idle',
                            i, timestamp=1234567 + i, host='com.example.www')
            handler.process(metric)
        patch_request.stop()

        expected_result = \
            'cpu,host=com.example.www total.idle=0.0 1234567\n' + \
            'cpu,host=com.example.www total.idle=1.0 1234568\n' + \
            'cpu,host=com.example.www total.idle=2.0 1234569\n'

        self.assertEqual(request_mock.call_count, 1)
        self.assertEqual(request_mock.call_args[1]['data'], expected_result)

    @run_only_if_influxdb_is_available
    def test_single_metric_process_v_0_8(self):
        config = configobj.ConfigObj()
        config['influxdb_version'] = '0.8'
        config['batch_size'] = 1

        metric = Metric('servers.com.example.www.cpu.total.idle',
                        0, timestamp=1234567, host='will-be-ignored')

        handler = InfluxdbHandler(config)
        handler.time_multiplier = float('-inf')

        request_mock = Mock()
        patch_request = patch.object(handler.influx, 'request', request_mock)
        patch_request.start()
        handler.process(metric)
        patch_request.stop()

        expected_result = [dict(columns=['time', 'value'],
                                name='servers.com.example.www.cpu.total.idle',
                                points=[[1234567, 0.0]])]

        self.assertEqual(request_mock.call_count, 1)
        self.assertEqual(request_mock.call_args[1]['data'], expected_result)

    @run_only_if_influxdb_is_available
    def test_multiple_metric_process_v_0_8(self):
        config = configobj.ConfigObj()
        config['influxdb_version'] = '0.8'
        num = 3
        config['batch_size'] = num

        handler = InfluxdbHandler(config)
        handler.time_multiplier = float('-inf')

        request_mock = Mock()
        patch_request = patch.object(handler.influx, 'request', request_mock)
        patch_request.start()
        for i in range(num):
            metric = Metric('servers.com.example.www.cpu.total.idle',
                            i, timestamp=1234567 + i, host='will-be-ignored')
            handler.process(metric)
        patch_request.stop()

        expected_result = [dict(columns=['time', 'value'],
                                name='servers.com.example.www.cpu.total.idle',
                                points=[[1234567, 0.0], [1234568, 1.0],
                                        [1234569, 2.0]])]

        self.assertEqual(request_mock.call_count, 1)
        self.assertEqual(request_mock.call_args[1]['data'], expected_result)
