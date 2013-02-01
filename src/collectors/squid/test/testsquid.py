#!/usr/bin/python
# coding=utf-8
################################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import Mock
from mock import patch

from diamond.collector import Collector
from squid import SquidCollector

################################################################################


class TestSquidCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('SquidCollector', {
            'interval': 1,
        })

        self.collector = SquidCollector(config, None)

    def test_import(self):
        self.assertTrue(SquidCollector)

    @patch.object(Collector, 'publish')
    def test_should_work_with_fake_data(self, publish_mock):
        _getData_mock = patch.object(SquidCollector, '_getData', Mock(
                return_value=self.getFixture('fake_counters_1').getvalue()))
        _getData_mock.start()
        self.collector.collect()
        _getData_mock.stop()

        self.assertPublishedMany(publish_mock, {})

        _getData_mock = patch.object(SquidCollector, '_getData', Mock(
                return_value=self.getFixture('fake_counters_2').getvalue()))
        _getData_mock.start()
        self.collector.collect()
        _getData_mock.stop()

        metrics = {
            '3128.client_http.requests': 1,
            '3128.client_http.hits': 2,
            '3128.client_http.errors': 3,
            '3128.client_http.kbytes_in': 4,
            '3128.client_http.kbytes_out': 5,
            '3128.client_http.hit_kbytes_out': 6,
            '3128.server.all.requests': 7,
            '3128.server.all.errors': 8,
            '3128.server.all.kbytes_in': 9,
            '3128.server.all.kbytes_out': 10,
            '3128.server.http.requests': 1,
            '3128.server.http.errors': 12,
            '3128.server.http.kbytes_in': 13,
            '3128.server.http.kbytes_out': 14,
            '3128.server.ftp.requests': 15,
            '3128.server.ftp.errors': 16,
            '3128.server.ftp.kbytes_in': 17,
            '3128.server.ftp.kbytes_out': 18,
            '3128.server.other.requests': 19,
            '3128.server.other.errors': 20,
            '3128.server.other.kbytes_in': 21,
            '3128.server.other.kbytes_out': 22,
            '3128.icp.pkts_sent': 23,
            '3128.icp.pkts_recv': 24,
            '3128.icp.queries_sent': 25,
            '3128.icp.replies_sent': 26,
            '3128.icp.queries_recv': 27,
            '3128.icp.replies_recv': 28,
            '3128.icp.query_timeouts': 29,
            '3128.icp.replies_queued': 30,
            '3128.icp.kbytes_sent': 31,
            '3128.icp.kbytes_recv': 32,
            '3128.icp.q_kbytes_sent': 33,
            '3128.icp.r_kbytes_sent': 34,
            '3128.icp.q_kbytes_recv': 35,
            '3128.icp.r_kbytes_recv': 36,
            '3128.icp.times_used': 37,
            '3128.cd.times_used': 38,
            '3128.cd.msgs_sent': 39,
            '3128.cd.msgs_recv': 40,
            '3128.cd.memory': 41,
            '3128.cd.local_memory': 42,
            '3128.cd.kbytes_sent': 43,
            '3128.cd.kbytes_recv': 44,
            '3128.unlink.requests': 45,
            '3128.page_faults': 46,
            '3128.select_loops': 47,
            '3128.cpu_time': 48.1234567890,
            '3128.wall_time': 49.1234567890,
            '3128.swap.outs': 50,
            '3128.swap.ins': 51,
            '3128.swap.files_cleaned': 52,
            '3128.aborted_requests': 53
        }

        self.assertPublishedMany(publish_mock, metrics)

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        _getData_mock = patch.object(SquidCollector, '_getData', Mock(
                return_value=self.getFixture('counters_1').getvalue()))
        _getData_mock.start()
        self.collector.collect()
        _getData_mock.stop()

        self.assertPublishedMany(publish_mock, {})

        _getData_mock = patch.object(SquidCollector, '_getData', Mock(
                return_value=self.getFixture('counters_2').getvalue()))
        _getData_mock.start()
        self.collector.collect()
        _getData_mock.stop()

        metrics = {
            '3128.client_http.requests': 2,
            '3128.client_http.hits': 1,
            '3128.client_http.errors': 0,
            '3128.client_http.kbytes_in': 1,
            '3128.client_http.kbytes_out': 12.0,
            '3128.client_http.hit_kbytes_out': 10,
            '3128.server.all.requests': 0,
            '3128.server.all.errors': 0,
            '3128.server.all.kbytes_in': 0,
            '3128.server.all.kbytes_out': 0,
            '3128.server.http.requests': 0,
            '3128.server.http.errors': 0,
            '3128.server.http.kbytes_in': 0,
            '3128.server.http.kbytes_out': 0,
            '3128.server.ftp.requests': 0,
            '3128.server.ftp.errors': 0,
            '3128.server.ftp.kbytes_in': 0,
            '3128.server.ftp.kbytes_out': 0,
            '3128.server.other.requests': 0,
            '3128.server.other.errors': 0,
            '3128.server.other.kbytes_in': 0,
            '3128.server.other.kbytes_out': 0,
            '3128.icp.pkts_sent': 0,
            '3128.icp.pkts_recv': 0,
            '3128.icp.queries_sent': 0,
            '3128.icp.replies_sent': 0,
            '3128.icp.queries_recv': 0,
            '3128.icp.replies_recv': 0,
            '3128.icp.query_timeouts': 0,
            '3128.icp.replies_queued': 0,
            '3128.icp.kbytes_sent': 0,
            '3128.icp.kbytes_recv': 0,
            '3128.icp.q_kbytes_sent': 0,
            '3128.icp.r_kbytes_sent': 0,
            '3128.icp.q_kbytes_recv': 0,
            '3128.icp.r_kbytes_recv': 0,
            '3128.icp.times_used': 0,
            '3128.cd.times_used': 0,
            '3128.cd.msgs_sent': 0,
            '3128.cd.msgs_recv': 0,
            '3128.cd.memory': 0,
            '3128.cd.local_memory': 0,
            '3128.cd.kbytes_sent': 0,
            '3128.cd.kbytes_recv': 0,
            '3128.unlink.requests': 0,
            '3128.page_faults': 0,
            '3128.select_loops': 10827.0,
            '3128.cpu_time': 0,
            '3128.wall_time': 10,
            '3128.swap.outs': 0,
            '3128.swap.ins': 2,
            '3128.swap.files_cleaned': 0,
            '3128.aborted_requests': 0
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

################################################################################
if __name__ == "__main__":
    unittest.main()
