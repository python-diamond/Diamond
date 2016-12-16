#!/usr/bin/python
# coding=utf-8
##########################################################################

from diamond.collector import Collector
from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import patch
from mock import Mock

from etcdstat import EtcdCollector

try:
    import simplejson as json
except ImportError:
    import json

##########################################################################


class TestEtcdCollector(CollectorTestCase):

    def setUp(self):
        config = get_collector_config('EtcdCollector', {
            'interval': 10
        })

        self.collector = EtcdCollector(config, None)

    def test_import(self):
        self.assertTrue(EtcdCollector)

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_follower_data(self, publish_mock):
        patch1_collector = patch.object(
            EtcdCollector,
            'get_self_metrics',
            Mock(return_value=json.loads(
                 self.getFixture('follower-self-metrics.json').getvalue())))

        patch2_collector = patch.object(
            EtcdCollector,
            'get_store_metrics',
            Mock(return_value=json.loads(
                 self.getFixture('store-metrics2.json').getvalue())))

        patch1_collector.start()
        patch2_collector.start()
        self.collector.collect()
        patch2_collector.stop()
        patch1_collector.stop()

        metrics = {
            'self.is_leader': 0,
            'self.sendAppendRequestCnt': 0,
            'self.recvAppendRequestCnt': 79367,
            'self.recvPkgRate': 6.557436727874493,
            'self.recvBandwidthRate': 527.021189819273,
            'store.compareAndDeleteFail': 0,
            'store.watchers': 0,
            'store.setsFail': 12,
            'store.createSuccess': 1294,
            'store.compareAndSwapFail': 136,
            'store.compareAndSwapSuccess': 4839,
            'store.deleteSuccess': 6,
            'store.updateSuccess': 2,
            'store.createFail': 0,
            'store.getsSuccess': 396632,
            'store.expireCount': 0,
            'store.deleteFail': 6,
            'store.updateFail': 0,
            'store.getsFail': 255837,
            'store.compareAndDeleteSuccess': 1239,
            'store.setsSuccess': 98571,
        }

        self.assertPublishedMany(publish_mock, metrics)

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_leader_data(self, publish_mock):
        patch1_collector = patch.object(
            EtcdCollector,
            'get_self_metrics',
            Mock(return_value=json.loads(
                 self.getFixture('leader-self-metrics.json').getvalue())))

        patch2_collector = patch.object(
            EtcdCollector,
            'get_store_metrics',
            Mock(return_value=json.loads(
                 self.getFixture('store-metrics.json').getvalue())))

        patch1_collector.start()
        patch2_collector.start()
        self.collector.collect()
        patch2_collector.stop()
        patch1_collector.stop()

        metrics = {
            'self.is_leader': 1,
            'self.sendAppendRequestCnt': 2097127,
            'self.recvAppendRequestCnt': 5870,
            'self.sendPkgRate': 11.763588080610418,
            'self.sendBandwidthRate': 901.0908469747579,
            'store.compareAndDeleteFail': 0,
            'store.watchers': 51,
            'store.setsFail': 123,
            'store.createSuccess': 6468,
            'store.compareAndSwapFail': 355,
            'store.compareAndSwapSuccess': 9156,
            'store.deleteSuccess': 2468,
            'store.updateSuccess': 4576,
            'store.createFail': 2508,
            'store.getsSuccess': 1685131,
            'store.expireCount': 0,
            'store.deleteFail': 2138,
            'store.updateFail': 0,
            'store.getsFail': 922428,
            'store.compareAndDeleteSuccess': 2047,
            'store.setsSuccess': 733,
        }

        self.assertPublishedMany(publish_mock, metrics)

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])

##########################################################################
if __name__ == "__main__":
    unittest.main()
