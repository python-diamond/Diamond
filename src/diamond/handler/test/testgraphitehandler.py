#!/usr/bin/python
# coding=utf-8
################################################################################

from test import unittest
from mock import Mock
from mock import patch
from mock import call

import configobj

from diamond.handler.graphite import GraphiteHandler
from diamond.metric import Metric


class TestGraphiteHandler(unittest.TestCase):

    def test_single_metric(self):
        config = configobj.ConfigObj()
        config['host'] = 'graphite.example.com'
        config['batch'] = 1

        metric = Metric('servers.com.example.www.cpu.total.idle',
                        0, timestamp=1234567, host='will-be-ignored')

        expected_data = [
            call("servers.com.example.www.cpu.total.idle 0 1234567\n"),
        ]

        handler = GraphiteHandler(config)

        patch_sock = patch.object(handler, 'socket', True)
        sendmock = Mock()
        patch_send = patch.object(GraphiteHandler, '_send_data', sendmock)

        patch_sock.start()
        patch_send.start()
        handler.process(metric)
        patch_send.stop()
        patch_sock.stop()

        self.assertEqual(sendmock.call_count, len(expected_data))
        self.assertEqual(sendmock.call_args_list, expected_data)

    def test_multi_no_batching(self):
        config = configobj.ConfigObj()
        config['host'] = 'graphite.example.com'
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

        handler = GraphiteHandler(config)

        patch_sock = patch.object(handler, 'socket', True)
        sendmock = Mock()
        patch_send = patch.object(GraphiteHandler, '_send_data', sendmock)

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
        config['host'] = 'graphite.example.com'
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

        handler = GraphiteHandler(config)

        patch_sock = patch.object(handler, 'socket', True)
        sendmock = Mock()
        patch_send = patch.object(GraphiteHandler, '_send_data', sendmock)

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
        config['host'] = 'graphite.example.com'
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

        handler = GraphiteHandler(config)

        # simulate an unreachable graphite host
        # thus force backlog functionality
        connect_mock = Mock()
        patch_connect = patch.object(GraphiteHandler, '_connect', connect_mock)
        send_mock = Mock()
        patch_send = patch.object(GraphiteHandler, '_send_data', send_mock)

        patch_connect.start()
        patch_send.start()
        for m in metrics:
            handler.process(m)
        patch_send.stop()
        patch_connect.stop()

        self.assertEqual(connect_mock.call_count, len(metrics))
        self.assertEqual(send_mock.call_count, 0)
        self.assertEqual(handler.metrics, expected_data)


if __name__ == "__main__":
    unittest.main()
