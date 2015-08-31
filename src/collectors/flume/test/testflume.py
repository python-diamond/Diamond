#!/usr/bin/python
# coding=utf-8

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import patch
from mock import Mock

from diamond.collector import Collector
from flume import FlumeCollector


class TestFlumeCollector(CollectorTestCase):

    def setUp(self):
        config = get_collector_config('FlumeCollector', {
            'interval': 10
        })

        self.collector = FlumeCollector(config, None)

    def test_import(self):
        self.assertTrue(FlumeCollector)

    @patch.object(Collector, 'publish')
    @patch.object(Collector, 'publish_gauge')
    @patch.object(Collector, 'publish_counter')
    def test_collect_should_work(self,
                                 publish_mock,
                                 publish_gauge_mock,
                                 publish_counter_mock):
        patch_urlopen = patch('urllib2.urlopen',
                              Mock(return_value=self.getFixture('metrics')))

        patch_urlopen.start()
        self.collector.collect()
        patch_urlopen.stop()

        metrics = {
            'CHANNEL.channel1.ChannelFillPercentage': 0.0,
            'CHANNEL.channel1.EventPutAttempt': 50272828,
            'CHANNEL.channel1.EventPutSuccess': 50255318,
            'CHANNEL.channel1.EventTakeAttempt': 50409933,
            'CHANNEL.channel1.EventTakeSuccess': 50255318,
            'SINK.sink1.BatchComplete': 251705,
            'SINK.sink1.BatchEmpty': 76250,
            'SINK.sink1.BatchUnderflow': 379,
            'SINK.sink1.ConnectionClosed': 6,
            'SINK.sink1.ConnectionCreated': 7,
            'SINK.sink1.ConnectionFailed': 0,
            'SINK.sink1.EventDrainAttempt': 25190171,
            'SINK.sink1.EventDrainSuccess': 25189571,
            'SOURCE.source1.AppendAccepted': 0,
            'SOURCE.source1.AppendBatchAccepted': 56227,
            'SOURCE.source1.AppendBatchReceived': 56258,
            'SOURCE.source1.AppendReceived': 0,
            'SOURCE.source1.EventAccepted': 50282681,
            'SOURCE.source1.EventReceived': 50311681,
            'SOURCE.source1.OpenConnection': 0
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany([publish_mock,
                                  publish_gauge_mock,
                                  publish_counter_mock
                                  ], metrics)

    @patch.object(Collector, 'publish')
    def test_blank_should_fail_gracefully(self, publish_mock):
        patch_urlopen = patch('urllib2.urlopen', Mock(
            return_value=self.getFixture('metrics_blank')))

        patch_urlopen.start()
        self.collector.collect()
        patch_urlopen.stop()

        self.assertPublishedMany(publish_mock, {})

    @patch.object(Collector, 'publish')
    def test_invalid_should_fail_gracefully(self, publish_mock):
        patch_urlopen = patch(
            'urllib2.urlopen',
            Mock(return_value=self.getFixture('metrics_invalid')))

        patch_urlopen.start()
        self.collector.collect()
        patch_urlopen.stop()

        self.assertPublishedMany(publish_mock, {})

if __name__ == "__main__":
    unittest.main()
