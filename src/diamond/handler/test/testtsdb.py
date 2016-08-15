#!/usr/bin/python
# coding=utf-8
##########################################################################

from test import unittest
from mock import Mock

import configobj

from diamond.handler.tsdb import TSDBHandler
import diamond.handler.tsdb as mod
from diamond.metric import Metric


# These two methods are used for overriding the TSDBHandler._connect method.
# Please check the Test class' setUp and tearDown methods
def fake_connect(self):
    # used for 'we can connect' tests
    m = Mock()
    self.socket = m
    if '__sockets_created' not in self.config:
        self.config['__sockets_created'] = [m]
    else:
        self.config['__sockets_created'].append(m)


def fake_bad_connect(self):
    # used for 'we can not connect' tests
    self.socket = None


class TestTSDBdHandler(unittest.TestCase):
    def setUp(self):
        self.__connect_method = mod.TSDBHandler
        mod.TSDBHandler._connect = fake_connect

    def tearDown(self):
        # restore the override
        mod.TSDBHandler._connect = self.__connect_method

    def test_single_gauge(self):
        config = configobj.ConfigObj()
        config['host'] = 'localhost'
        config['port'] = '9999'

        metric = Metric('servers.myhostname.cpu.cpu_count',
                        123, raw_value=123, timestamp=1234567,
                        host='myhostname', metric_type='GAUGE')

        expected_data = ('put cpu.cpu_count 1234567 123 hostname=myhostname\n')

        handler = TSDBHandler(config)
        handler.process(metric)
        handler.socket.sendall.assert_called_with(expected_data)

    def test_with_single_tag_no_space_in_front(self):
        config = configobj.ConfigObj()
        config['host'] = 'localhost'
        config['port'] = '9999'
        config['tags'] = 'myTag=myValue'

        metric = Metric('servers.myhostname.cpu.cpu_count',
                        123, raw_value=123, timestamp=1234567,
                        host='myhostname', metric_type='GAUGE')

        expected_data = 'put cpu.cpu_count 1234567 123 hostname=myhostname '
        expected_data += 'myTag=myValue\n'

        handler = TSDBHandler(config)
        handler.process(metric)
        handler.socket.sendall.assert_called_with(expected_data)

    def test_with_single_tag_space_in_front(self):
        config = configobj.ConfigObj()
        config['host'] = 'localhost'
        config['port'] = '9999'
        config['tags'] = ' myTag=myValue'

        metric = Metric('servers.myhostname.cpu.cpu_count',
                        123, raw_value=123, timestamp=1234567,
                        host='myhostname', metric_type='GAUGE')

        expected_data = 'put cpu.cpu_count 1234567 123 hostname=myhostname '
        expected_data += 'myTag=myValue\n'

        handler = TSDBHandler(config)
        handler.process(metric)
        handler.socket.sendall.assert_called_with(expected_data)

    def test_with_multiple_tag_no_space_in_front(self):
        config = configobj.ConfigObj()
        config['host'] = 'localhost'
        config['port'] = '9999'
        config['tags'] = 'myTag=myValue mySecondTag=myOtherValue'

        metric = Metric('servers.myhostname.cpu.cpu_count',
                        123, raw_value=123, timestamp=1234567,
                        host='myhostname', metric_type='GAUGE')

        expected_data = 'put cpu.cpu_count 1234567 123 hostname=myhostname '
        expected_data += 'myTag=myValue mySecondTag=myOtherValue\n'

        handler = TSDBHandler(config)
        handler.process(metric)
        handler.socket.sendall.assert_called_with(expected_data)

    def test_with_multiple_tag_space_in_front(self):
        config = configobj.ConfigObj()
        config['host'] = 'localhost'
        config['port'] = '9999'
        config['tags'] = ' myTag=myValue mySecondTag=myOtherValue'

        metric = Metric('servers.myhostname.cpu.cpu_count',
                        123, raw_value=123, timestamp=1234567,
                        host='myhostname', metric_type='GAUGE')

        expected_data = 'put cpu.cpu_count 1234567 123 hostname=myhostname '
        expected_data += 'myTag=myValue mySecondTag=myOtherValue\n'

        handler = TSDBHandler(config)
        handler.process(metric)
        handler.socket.sendall.assert_called_with(expected_data)

    def test_with_multiple_tag_no_space_in_front_comma(self):
        config = configobj.ConfigObj()
        config['host'] = 'localhost'
        config['port'] = '9999'
        config['tags'] = ['myFirstTag=myValue', 'mySecondTag=myOtherValue']

        metric = Metric('servers.myhostname.cpu.cpu_count',
                        123, raw_value=123, timestamp=1234567,
                        host='myhostname', metric_type='GAUGE')

        expected_data = 'put cpu.cpu_count 1234567 123 hostname=myhostname '
        expected_data += 'myFirstTag=myValue mySecondTag=myOtherValue\n'

        handler = TSDBHandler(config)
        handler.process(metric)
        handler.socket.sendall.assert_called_with(expected_data)

    def test_with_multiple_tag_no_space_in_front_comma_and_space(self):
        config = configobj.ConfigObj()
        config['host'] = 'localhost'
        config['port'] = '9999'
        config['tags'] = ['myFirstTag=myValue',
                          'mySecondTag=myOtherValue myThirdTag=yetAnotherVal']

        metric = Metric('servers.myhostname.cpu.cpu_count',
                        123, raw_value=123, timestamp=1234567,
                        host='myhostname', metric_type='GAUGE')

        expected_data = 'put cpu.cpu_count 1234567 123 hostname=myhostname '
        expected_data += 'myFirstTag=myValue mySecondTag=myOtherValue '
        expected_data += 'myThirdTag=yetAnotherVal\n'

        handler = TSDBHandler(config)
        handler.process(metric)
        handler.socket.sendall.assert_called_with(expected_data)
