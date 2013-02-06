#!/usr/bin/python
# coding=utf-8
################################################################################

import os
import sys

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from test import run_only
from mock import patch

from diamond.collector import Collector
from userscripts import UserScriptsCollector

################################################################################


def run_only_if_kitchen_is_available(func):
    if sys.version_info < (2, 7):
        try:
            from kitchen.pycompat27 import subprocess
            subprocess  # workaround for pyflakes issue #13
        except ImportError:
            subprocess = None
    else:
        import subprocess
    pred = lambda: subprocess is not None
    return run_only(func, pred)


class TestUserScriptsCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('UserScriptsCollector', {
            'interval': 10,
            'scripts_path': os.path.dirname(__file__) + '/fixtures/',
        })

        self.collector = UserScriptsCollector(config, None)

    def test_import(self):
        self.assertTrue(UserScriptsCollector)

    @run_only_if_kitchen_is_available
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
