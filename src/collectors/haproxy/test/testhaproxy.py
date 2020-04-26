#!/usr/bin/python
# coding=utf-8
##########################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import Mock
from mock import patch

from diamond.collector import Collector
from haproxy import HAProxyCollector

##########################################################################


class TestHAProxyCollector(CollectorTestCase):

    def setUp(self):
        config = get_collector_config('HAProxyCollector', {
            'interval': 10,
        })

        self.collector = HAProxyCollector(config, None)

    def test_import(self):
        self.assertTrue(HAProxyCollector)

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        self.collector.config['ignore_servers'] = False

        patch_urlopen = patch('urllib2.urlopen',
                              Mock(return_value=self.getFixture('stats.csv')))

        patch_urlopen.start()
        self.collector.collect()
        patch_urlopen.stop()

        metrics = self.getPickledResults('real_data.pkl')

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

    @patch.object(Collector, 'publish')
    def test_should_work_with_unix_socket_code_path(self, publish_mock):
        self.collector.config['method'] = 'unix'

        class MockSocket():
            def __init__(*args, **kwargs):
                self.connected = False
                self.output_data = ''

            def connect(*args, **kwargs):
                self.connected = True

            def send(obj, string, *args, **kwargs):
                if not self.connected:
                    raise Exception('MockSocket: Endpoint not connected.')
                if string == 'show stat\n':
                    self.output_data = self.getFixture('stats.csv').getvalue()

            def recv(obj, bufsize, *args, **kwargs):
                output_buffer = self.output_data[:bufsize]
                self.output_data = self.output_data[bufsize:]
                return output_buffer

        patch_socket = patch('socket.socket', Mock(return_value=MockSocket()))

        patch_socket.start()
        self.collector.collect()
        patch_socket.stop()

        metrics = self.getPickledResults('real_data.pkl')

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data_and_ignore_servers(self, publish_mock):
        self.collector.config['ignore_servers'] = True

        patch_urlopen = patch('urllib2.urlopen',
                              Mock(return_value=self.getFixture('stats.csv')))

        patch_urlopen.start()
        self.collector.collect()
        patch_urlopen.stop()

        metrics = self.getPickledResults('real_data_ignore_servers.pkl')

        self.assertPublishedMany(publish_mock, metrics)

##########################################################################
if __name__ == "__main__":
    unittest.main()
