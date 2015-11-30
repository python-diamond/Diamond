#!/usr/bin/python
# coding=utf-8
##########################################################################

import time

from test import unittest
from mock import Mock
from mock import patch
from mock import call

import configobj

import diamond.handler.graphite as mod
from diamond.metric import Metric


# These two methods are used for overriding the GraphiteHandler._connect method.
# Please check the Test class' setUp and tearDown methods
def fake_connect(self):
    # used for 'we can connect' tests
    self.socket = Mock()


def fake_bad_connect(self):
    # used for 'we can not connect' tests
    self.socket = None


class TestGraphiteHandler(unittest.TestCase):

    def setUp(self):
        self.__connect_method = mod.GraphiteHandler
        mod.GraphiteHandler._connect = fake_connect

    def tearDown(self):
        # restore the override
        mod.GraphiteHandler._connect = self.__connect_method

    def test_single_metric(self):
        config = configobj.ConfigObj()
        config['batch'] = 1

        metric = Metric('servers.com.example.www.cpu.total.idle',
                        0, timestamp=1234567, host='will-be-ignored')

        expected_data = [
            call("servers.com.example.www.cpu.total.idle 0 1234567\n"),
        ]

        handler = mod.GraphiteHandler(config)

        patch_sock = patch.object(handler, 'socket', True)
        sendmock = Mock()
        patch_send = patch.object(handler, '_send_data', sendmock)

        patch_sock.start()
        patch_send.start()
        handler.process(metric)
        patch_send.stop()
        patch_sock.stop()

        self.assertEqual(sendmock.call_count, len(expected_data))
        self.assertEqual(sendmock.call_args_list, expected_data)

    def test_multi_no_batching(self):
        config = configobj.ConfigObj()
        config['batch'] = 1

        metrics = [
            Metric('metricname1', 0, timestamp=123),
            Metric('metricname2', 0, timestamp=123),
            Metric('metricname3', 0, timestamp=123),
            Metric('metricname4', 0, timestamp=123),
        ]

        expected_data = [
            call("metricname1 0 123\n"),
            call("metricname2 0 123\n"),
            call("metricname3 0 123\n"),
            call("metricname4 0 123\n"),
        ]

        handler = mod.GraphiteHandler(config)

        patch_sock = patch.object(handler, 'socket', True)
        sendmock = Mock()
        patch_send = patch.object(handler, '_send_data', sendmock)

        patch_sock.start()
        patch_send.start()
        for m in metrics:
            handler.process(m)
        patch_send.stop()
        patch_sock.stop()

        self.assertEqual(sendmock.call_count, len(expected_data))
        self.assertEqual(sendmock.call_args_list, expected_data)

    def test_multi_with_batching(self):
        config = configobj.ConfigObj()
        config['batch'] = 2

        metrics = [
            Metric('metricname1', 0, timestamp=123),
            Metric('metricname2', 0, timestamp=123),
            Metric('metricname3', 0, timestamp=123),
            Metric('metricname4', 0, timestamp=123),
        ]

        expected_data = [
            call("metricname1 0 123\nmetricname2 0 123\n"),
            call("metricname3 0 123\nmetricname4 0 123\n"),
        ]

        handler = mod.GraphiteHandler(config)

        patch_sock = patch.object(handler, 'socket', True)
        sendmock = Mock()
        patch_send = patch.object(handler, '_send_data', sendmock)

        patch_sock.start()
        patch_send.start()
        for m in metrics:
            handler.process(m)
        patch_send.stop()
        patch_sock.stop()

        self.assertEqual(sendmock.call_count, len(expected_data))
        self.assertEqual(sendmock.call_args_list, expected_data)

    def test_backlog(self):
        config = configobj.ConfigObj()
        config['batch'] = 1

        # start trimming after X batchsizes in buffer
        config['max_backlog_multiplier'] = 4
        # when trimming: keep last X batchsizes
        config['trim_backlog_multiplier'] = 3

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
            "metricname6 0 123\n",
            "metricname7 0 123\n",
            "metricname8 0 123\n",
        ]

        # simulate an unreachable graphite host
        # thus force backlog functionality
        mod.GraphiteHandler._connect = fake_bad_connect
        handler = mod.GraphiteHandler(config)

        send_mock = Mock()
        patch_send = patch.object(handler, '_send_data', send_mock)

        patch_send.start()
        for m in metrics:
            handler.process(m)
        patch_send.stop()

        # self.assertEqual(connect_mock.call_count, len(metrics))
        self.assertEqual(send_mock.call_count, 0)
        self.assertEqual(handler.metrics, expected_data)

    def test_error_throttling(self):
        """
        This is more of a generic test checking that the _throttle_error method
        works as expected

        TODO: test that the graphite handler calls _throttle_error in the right
        circumstances.
        """
        config = configobj.ConfigObj()
        config['server_error_interval'] = '0.1'

        handler = mod.GraphiteHandler(config)

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
