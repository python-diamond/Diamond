#!/usr/bin/python
# coding=utf-8
################################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import Mock
from mock import patch

from diamond.collector import Collector

from ntpd import NtpdCollector

################################################################################


class TestNtpdCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('NtpdCollector', {})

        self.collector = NtpdCollector(config, None)

    def test_import(self):
        self.assertTrue(NtpdCollector)

    @patch.object(Collector, 'publish')
    def test_should_work_wtih_real_data(self, publish_mock):
        ntpq_data = Mock(return_value=self.getFixture('ntpq').getvalue())
        ntpdc_data = Mock(return_value=self.getFixture('ntpdc').getvalue())
        collector_mock = patch.multiple(NtpdCollector,
                                        get_ntpq_output=ntpq_data,
                                        get_ntpdc_output=ntpdc_data)

        collector_mock.start()
        self.collector.collect()
        collector_mock.stop()

        metrics = {
            'jitter': 0.026,
            'when': 39,
            'stratum': 2,
            'reach': 377,
            'delay': 0.127,
            'offset': -0.005,
            'poll': 1024,
            'max_error': 0.039793,
            'est_error': 5.1e-05,
            'frequency': -14.24,
            'offset': -5.427e-06,
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

    @patch.object(Collector, 'publish')
    def test_should_fail_gracefully(self, publish_mock):
        ntpq_data = Mock(return_value='')
        ntpdc_data = Mock(return_value='')
        collector_mock = patch.multiple(NtpdCollector,
                                        get_ntpq_output=ntpq_data,
                                        get_ntpdc_output=ntpdc_data)

        collector_mock.start()
        self.collector.collect()
        collector_mock.stop()

        self.assertPublishedMany(publish_mock, {})

################################################################################
if __name__ == "__main__":
    unittest.main()
