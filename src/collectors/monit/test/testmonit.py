#!/usr/bin/python
# coding=utf-8
################################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import Mock
from mock import patch

from diamond.collector import Collector

from monit import MonitCollector

################################################################################


class TestMonitCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('MonitCollector',
                                      {'byte_unit': 'kilobyte', })

        self.collector = MonitCollector(config, None)

    def test_import(self):
        self.assertTrue(MonitCollector)

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        patch_urlopen = patch('urllib2.urlopen', Mock(
            return_value=self.getFixture('status.xml')))

        patch_urlopen.start()
        self.collector.collect()
        patch_urlopen.stop()

        metrics = {
            'app_thin_8101.cpu.percent': 0.9,
            'app_thin_8101.memory.kilobyte_usage': 216104,
            'app_thin_8102.cpu.percent': 1.1,
            'app_thin_8102.memory.kilobyte_usage': 212736,
            'app_thin_8103.cpu.percent': 0.9,
            'app_thin_8103.memory.kilobyte_usage': 204948,
            'app_thin_8104.cpu.percent': 0.9,
            'app_thin_8104.memory.kilobyte_usage': 212464,
            'sshd.cpu.percent': 0.0,
            'sshd.memory.kilobyte_usage': 2588,
            'rsyslogd.cpu.percent': 0.0,
            'rsyslogd.memory.kilobyte_usage': 2664,
            'postfix.cpu.percent': 0.0,
            'postfix.memory.kilobyte_usage': 2304,
            'nginx.cpu.percent': 0.0,
            'nginx.memory.kilobyte_usage': 18684,
            'haproxy.cpu.percent': 0.0,
            'haproxy.memory.kilobyte_usage': 4040,
            'cron.cpu.percent': 0.0,
            'cron.memory.kilobyte_usage': 1036,
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

    @patch.object(Collector, 'publish')
    def test_should_fail_gracefully(self, publish_mock):
        patch_urlopen = patch('urllib2.urlopen',
                              Mock(
                                return_value=self.getFixture(
                                    'status_blank.xml')))

        patch_urlopen.start()
        self.collector.collect()
        patch_urlopen.stop()

        self.assertPublishedMany(publish_mock, {})

################################################################################
if __name__ == "__main__":
    unittest.main()
