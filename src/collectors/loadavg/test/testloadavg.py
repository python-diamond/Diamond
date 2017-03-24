#!/usr/bin/python
# coding=utf-8
##########################################################################

import os
from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from test import Mock
from test import patch
from test import StringIO
from test import BUILTIN_OPEN

from diamond.collector import Collector
from loadavg import LoadAverageCollector

##########################################################################


class TestLoadAverageCollector(CollectorTestCase):

    def setUp(self):
        config = get_collector_config('LoadAverageCollector', {
            'interval': 10
        })

        self.collector = LoadAverageCollector(config, None)

    def test_import(self):
        self.assertTrue(LoadAverageCollector)

    @patch(BUILTIN_OPEN)
    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_open_proc_loadavg(self, publish_mock, open_mock):
        if not os.path.exists('/proc/loadavg'):
            # on platforms that don't provide /proc/loadavg: don't bother
            # testing this.
            return
        open_mock.return_value = StringIO('')
        self.collector.collect()
        open_mock.assert_called_once_with('/proc/loadavg')

    @patch('multiprocessing.cpu_count')
    @patch('os.getloadavg')
    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock, getloadavg_mock,
                                        cpu_count_mock):
        LoadAverageCollector.PROC_LOADAVG = self.getFixturePath('proc_loadavg')
        getloadavg_mock.return_value = (0.12, 0.23, 0.34)
        cpu_count_mock.return_value = 2
        self.collector.collect()

        metrics = {
            '01': (0.12, 2),
            '05': (0.23, 2),
            '15': (0.34, 2),
            '01_normalized': (0.06, 2),
            '05_normalized': (0.115, 2),
            '15_normalized': (0.17, 2),
            'processes_running': 1,
            'processes_total': 235
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

##########################################################################
if __name__ == "__main__":
    unittest.main()
