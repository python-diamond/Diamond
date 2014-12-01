#!/usr/bin/python
# coding=utf-8
################################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from test import run_only
from mock import patch

from diamond.collector import Collector
from users import UsersCollector

import sys


################################################################################


def run_only_if_pyutmp_is_available(func):
    try:
        import pyutmp
    except ImportError:
        pyutmp = None
    try:
        import utmp
    except ImportError:
        utmp = None
    pred = lambda: pyutmp is not None or utmp is not None
    return run_only(func, pred)


class TestUsersCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('UsersCollector', {
            'utmp': self.getFixturePath('utmp.centos6'),
        })

        self.collector = UsersCollector(config, None)

    def test_import(self):
        self.assertTrue(UsersCollector)

    @run_only_if_pyutmp_is_available
    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):

        metrics = {
            'kormoc':   2,
            'root':     3,
            'total':    5,
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])

        # Because of the compiled nature of pyutmp, we can't actually test
        # different operating system versions then the currently running
        # one
        if sys.platform.startswith('linux'):
            self.collector.collect()

            self.assertPublishedMany(publish_mock, metrics)

################################################################################
if __name__ == "__main__":
    unittest.main()
