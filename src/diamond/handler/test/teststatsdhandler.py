#!/usr/bin/python
# coding=utf-8
################################################################################

from test import unittest
from test import run_only
from mock import patch
from mock import ANY

import configobj

from diamond.handler.stats_d import StatsdHandler
from diamond.metric import Metric


def run_only_if_statsd_is_available(func):
    try:
        import statsd
    except ImportError:
        statsd = None
    pred = lambda: statsd is not None
    return run_only(func, pred)


class TestStatsdHandler(unittest.TestCase):

    @run_only_if_statsd_is_available
    @patch('statsd.Client')
    def test_single_gauge(self, mock_client):
        instance = mock_client.return_value
        instance._send.return_value = 1

        config = configobj.ConfigObj()
        config['host'] = 'localhost'
        config['port'] = '9999'
        config['batch'] = 1

        metric = Metric('servers.com.example.www.cpu.total.idle',
                        123, raw_value=123, timestamp=1234567,
                        host='will-be-ignored', metric_type='GAUGE')

        expected_data = {
            'servers.com.example.www.cpu.total.idle': '123|g'
        }

        handler = StatsdHandler(config)
        handler.process(metric)
        mock_client._send.assert_called_with(ANY, expected_data)

    @run_only_if_statsd_is_available
    @patch('statsd.Client')
    def test_single_counter(self, mock_client):
        instance = mock_client.return_value
        instance._send.return_value = 1

        config = configobj.ConfigObj()
        config['host'] = 'localhost'
        config['port'] = '9999'
        config['batch'] = 1

        metric = Metric('servers.com.example.www.cpu.total.idle',
                        5, raw_value=123, timestamp=1234567,
                        host='will-be-ignored', metric_type='COUNTER')

        expected_data = {
            'servers.com.example.www.cpu.total.idle': '123|c'
        }

        handler = StatsdHandler(config)
        handler.process(metric)
        mock_client._send.assert_called_with(ANY, expected_data)

    @run_only_if_statsd_is_available
    @patch('statsd.Client')
    def test_multiple_counter(self, mock_client):
        instance = mock_client.return_value
        instance._send.return_value = 1

        config = configobj.ConfigObj()
        config['host'] = 'localhost'
        config['port'] = '9999'
        config['batch'] = 1

        metric1 = Metric('servers.com.example.www.cpu.total.idle',
                         5, raw_value=123, timestamp=1234567,
                         host='will-be-ignored', metric_type='COUNTER')

        metric2 = Metric('servers.com.example.www.cpu.total.idle',
                         7, raw_value=128, timestamp=1234567,
                         host='will-be-ignored', metric_type='COUNTER')

        expected_data1 = {
            'servers.com.example.www.cpu.total.idle': '123|c'
        }

        expected_data2 = {
            'servers.com.example.www.cpu.total.idle': '5|c'
        }

        handler = StatsdHandler(config)
        handler.process(metric1)
        mock_client._send.assert_called_with(ANY, expected_data1)

        handler.process(metric2)
        mock_client._send.assert_called_with(ANY, expected_data2)
