#!/usr/bin/python
# coding=utf-8
##########################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import Mock
from mock import patch

from diamond.collector import Collector

from nginx import NginxCollector

##########################################################################


class TestNginxCollector(CollectorTestCase):

    def setUp(self):
        config = get_collector_config('NginxCollector', {})

        self.collector = NginxCollector(config, None)

    def test_import(self):
        self.assertTrue(NginxCollector)

    @patch.object(Collector, 'publish')
    @patch.object(Collector, 'publish_gauge')
    @patch.object(Collector, 'publish_counter')
    def test_should_work_with_real_data(self, publish_counter_mock,
                                        publish_gauge_mock, publish_mock):

        mockMimeMessage = Mock(**{'gettype.return_value': 'text/html'})
        mockResponse = Mock(**{
            'readlines.return_value': self.getFixture('status').readlines(),
            'info.return_value': mockMimeMessage,
            }
        )

        patch_urlopen = patch('urllib2.urlopen', Mock(
            return_value=mockResponse))

        patch_urlopen.start()
        self.collector.collect()
        patch_urlopen.stop()

        metrics = {
            'active_connections': 3,
            'conn_accepted': 396396,
            'conn_handled': 396396,
            'req_handled': 396396,
            'act_reads': 2,
            'act_writes': 1,
            'act_waits': 0,
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany([publish_mock,
                                  publish_gauge_mock,
                                  publish_counter_mock
                                  ], metrics)

    @patch.object(Collector, 'publish')
    @patch.object(Collector, 'publish_gauge')
    @patch.object(Collector, 'publish_counter')
    def test_plus_should_work_with_real_data(self, publish_counter_mock,
                                             publish_gauge_mock, publish_mock):

        mockMimeMessage = Mock(**{'gettype.return_value': 'application/json'})
        mockResponse = Mock(**{
            'readlines.return_value':
                self.getFixture('plus_status').readlines(),
            'info.return_value': mockMimeMessage,
            'read.return_value': self.getFixture('plus_status').read(),
            }
        )

        patch_urlopen = patch('urllib2.urlopen', Mock(
            return_value=mockResponse))

        patch_urlopen.start()
        self.collector.collect()
        patch_urlopen.stop()

        metrics = {
            'conn.active': 11,
            'conn.accepted': 25512010,
            'conn.dropped': 0,
            'conn.idle': 30225,

            'req.current': 11,
            'req.total': 1061989107,

            'ssl.handshakes': 0,
            'ssl.session_reuses': 0,
            'ssl.handshakes_failed': 0,

            'servers.www.processing': 10,
            'servers.www.received': 1869206012545,
            'servers.www.discarded': 2433140,
            'servers.www.requests': 1061980757,
            'servers.www.sent': 169151943651,

            'servers.app_com.processing': 3,
            'servers.app_com.received': 100,
            'servers.app_com.discarded': 5,
            'servers.app_com.requests': 25,
            'servers.app_com.sent': 293752,

            'servers.www.responses.1xx': 0,
            'servers.www.responses.2xx': 1058969631,
            'servers.www.responses.3xx': 363,
            'servers.www.responses.4xx': 396193,
            'servers.www.responses.5xx': 181420,
            'servers.www.responses.total': 1059547607,

            'servers.app_com.responses.1xx': 0,
            'servers.app_com.responses.2xx': 100,
            'servers.app_com.responses.3xx': 3,
            'servers.app_com.responses.4xx': 4,
            'servers.app_com.responses.5xx': 0,
            'servers.app_com.responses.total': 107,

            'upstreams.www-upstream.keepalive': 225,
            'upstreams.www-upstream.peers.1_1_1_94-8080.active': 1,
            'upstreams.www-upstream.peers.1_1_1_94-8080.downtime': 0,
            'upstreams.www-upstream.peers.1_1_1_94-8080.fails': 1534,
            'upstreams.www-upstream.peers.1_1_1_94-8080.max_conns': 540,
            'upstreams.www-upstream.peers.1_1_1_94-8080.received': 1301376667,
            'upstreams.www-upstream.peers.1_1_1_94-8080.requests': 106379240,
            'upstreams.www-upstream.peers.1_1_1_94-8080.sent': 188216479779,
            'upstreams.www-upstream.peers.1_1_1_94-8080.unavail': 0,

            'upstreams.www-upstream.peers.1_1_1_94-8080.responses.1xx': 0,
            'upstreams.www-upstream.peers.1_1_1_94-8080.responses.2xx':
                106277550,
            'upstreams.www-upstream.peers.1_1_1_94-8080.responses.3xx': 33,
            'upstreams.www-upstream.peers.1_1_1_94-8080.responses.4xx': 39694,
            'upstreams.www-upstream.peers.1_1_1_94-8080.responses.5xx': 0,
            'upstreams.www-upstream.peers.1_1_1_94-8080.responses.total':
                106317277,

            'upstreams.app_upstream.keepalive': 0,
            'upstreams.app_upstream.peers.1_2_5_3-8080.active': 0,
            'upstreams.app_upstream.peers.1_2_5_3-8080.downtime': 0,
            'upstreams.app_upstream.peers.1_2_5_3-8080.fails': 0,
            'upstreams.app_upstream.peers.1_2_5_3-8080.received': 792,
            'upstreams.app_upstream.peers.1_2_5_3-8080.requests': 4,
            'upstreams.app_upstream.peers.1_2_5_3-8080.sent': 571,
            'upstreams.app_upstream.peers.1_2_5_3-8080.unavail': 0,

            'upstreams.app_upstream.peers.1_2_5_8-8080.responses.1xx': 0,
            'upstreams.app_upstream.peers.1_2_5_8-8080.responses.2xx': 2,
            'upstreams.app_upstream.peers.1_2_5_8-8080.responses.3xx': 0,
            'upstreams.app_upstream.peers.1_2_5_8-8080.responses.4xx': 1,
            'upstreams.app_upstream.peers.1_2_5_8-8080.responses.5xx': 0,
            'upstreams.app_upstream.peers.1_2_5_8-8080.responses.total': 3,

        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany([publish_mock,
                                  publish_gauge_mock,
                                  publish_counter_mock
                                  ], metrics)

    @patch.object(Collector, 'publish')
    def test_should_fail_gracefully(self, publish_mock):
        mockMimeMessage = Mock(**{'gettype.return_value': 'text/html'})
        mockResponse = Mock(**{
            'readlines.return_value':
                self.getFixture('status_blank').readlines(),
            'info.return_value': mockMimeMessage,
            }
        )

        patch_urlopen = patch('urllib2.urlopen', Mock(
            return_value=mockResponse))

        patch_urlopen.start()
        self.collector.collect()
        patch_urlopen.stop()

        self.assertPublishedMany(publish_mock, {})

##########################################################################
if __name__ == "__main__":
    unittest.main()
