#!/usr/bin/python
# coding=utf-8
################################################################################

import os

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import Mock
from mock import patch

from diamond.collector import Collector
from ksm import KSMCollector

################################################################################


class TestKSMCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('KSMCollector', {
            'interval': 10,
            'ksm_path': os.path.dirname(__file__) + '/fixtures/'
        })

        self.collector = KSMCollector(config, None)

    def test_import(self):
        self.assertTrue(KSMCollector)

    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_work_with_synthetic_data(self, publish_mock):
        self.collector.collect()

        metrics = {
            'full_scans': 123.0,
            'pages_shared': 124.0,
            'pages_sharing': 125.0,
            'pages_to_scan': 100.0,
            'pages_unshared': 126.0,
            'pages_volatile': 127.0,
            'run': 1.0,
            'sleep_millisecs': 20.0,
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

################################################################################
if __name__ == "__main__":
    unittest.main()
