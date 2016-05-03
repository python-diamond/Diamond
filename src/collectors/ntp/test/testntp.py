#!/usr/bin/python
# coding=utf-8
##########################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import Mock
from mock import patch

from diamond.collector import Collector

from ntp import NtpCollector

##########################################################################


class TestNtpCollector(CollectorTestCase):

    def setUp(self):
        config = get_collector_config('NtpCollector', {})

        self.collector = NtpCollector(config, None)

    def test_import(self):
        self.assertTrue(NtpCollector)

    @patch.object(Collector, 'publish')
    def test_should_work_wtih_real_data(self, publish_mock):
        ntpdate_data = Mock(
            return_value=(self.getFixture('ntpdate').getvalue(), None))
        collector_mock = patch.object(NtpCollector,
                                      'run_command',
                                      ntpdate_data)
        collector_mock.start()
        self.collector.collect()
        collector_mock.stop()

        metrics = {
            'server.count': 4,
            'offset.milliseconds': 0
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

    @patch.object(Collector, 'publish')
    def test_should_work_wtih_real_data_and_custom_config(self, publish_mock):
        config = get_collector_config('NtpCollector', {
            'time_scale': 'seconds',
            'precision': 3,
        })

        self.collector = NtpCollector(config, None)

        ntpdate_data = Mock(
            return_value=(self.getFixture('ntpdate').getvalue(), None))
        collector_mock = patch.object(NtpCollector,
                                      'run_command',
                                      ntpdate_data)
        collector_mock.start()
        self.collector.collect()
        collector_mock.stop()

        metrics = {
            'server.count': 4,
            'offset.seconds': -0.000128
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

    @patch.object(Collector, 'publish')
    def test_should_fail_gracefully(self, publish_mock):
        ntpdate_data = Mock(return_value=('', None))
        collector_mock = patch.object(NtpCollector,
                                      'run_command',
                                      ntpdate_data)

        collector_mock.start()
        self.collector.collect()
        collector_mock.stop()

        self.assertPublishedMany(publish_mock, {})

##########################################################################
if __name__ == "__main__":
    unittest.main()
