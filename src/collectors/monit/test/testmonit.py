#!/usr/bin/python
# coding=utf-8
################################################################################

from test import *

from diamond.collector import Collector

from monit import MonitCollector

################################################################################

class TestMonitCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('MonitCollector', {'byte_unit':    'kilobyte',})

        self.collector = MonitCollector(config, None)

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        with patch('urllib2.urlopen', Mock(return_value = self.getFixture('status.xml'))):
            self.collector.collect()

        metrics = {
            'app_thin_8101.cpu.percent': 0.9,
            'app_thin_8101.memory.kilobyte_usage': 216104,
            'app_thin_8102.cpu.percent': 1.1, 
            'app_thin_8102.memory.kilobyte_usage':212736,
            'app_thin_8103.cpu.percent': 0.9, 
            'app_thin_8103.memory.kilobyte_usage':204948,
            'app_thin_8104.cpu.percent': 0.9, 
            'app_thin_8104.memory.kilobyte_usage':212464,
            'sshd.cpu.percent': 0.0, 
            'sshd.memory.kilobyte_usage':2588,
            'rsyslogd.cpu.percent': 0.0, 
            'rsyslogd.memory.kilobyte_usage':2664,
            'postfix.cpu.percent': 0.0, 
            'postfix.memory.kilobyte_usage':2304,
            'nginx.cpu.percent': 0.0, 
            'nginx.memory.kilobyte_usage':18684,
            'haproxy.cpu.percent': 0.0, 
            'haproxy.memory.kilobyte_usage':4040,
            'cron.cpu.percent': 0.0, 
            'cron.memory.kilobyte_usage':1036,
        }

        self.setDocExample(self.collector.__class__.__name__, metrics)
        self.assertPublishedMany(publish_mock, metrics)

    @patch.object(Collector, 'publish')
    def test_should_fail_gracefully(self, publish_mock):
        with patch('urllib2.urlopen', Mock(return_value = self.getFixture('status_blank.xml'))):
            self.collector.collect()

        self.assertPublishedMany(publish_mock, {})

################################################################################
if __name__ == "__main__":
    unittest.main()
