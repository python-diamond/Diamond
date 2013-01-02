#!/usr/bin/python
# coding=utf-8
################################################################################

import os

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import patch

from diamond.collector import Collector
from userscripts import UserScriptsCollector

################################################################################


class TestUserScriptsCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('UserScriptsCollector', {
            'interval': 10,
            'scripts_path': os.path.dirname(__file__) + '/fixtures/',
        })

        self.collector = UserScriptsCollector(config, None)

    def test_import(self):
        self.assertTrue(UserScriptsCollector)

    @patch.object(Collector, 'publish')
    def test_should_work_with_example(self, publish_mock):
        self.collector.collect()

        metrics = {
            'example.1': 42,
            'example.2': 24,
            'example.3': 12.1212,
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics)
        self.assertPublishedMany(publish_mock, metrics)

################################################################################
if __name__ == "__main__":
    unittest.main()
