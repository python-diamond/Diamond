#!/usr/bin/python
# coding=utf-8
################################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import Mock
from mock import patch

from diamond.collector import Collector
from powerdns import PowerDNSCollector

################################################################################


class TestPowerDNSCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('PowerDNSCollector', {
            'interval': 1,
            'bin': 'true',
            'use_sudo': False,
        })

        self.collector = PowerDNSCollector(config, None)

    def test_import(self):
        self.assertTrue(PowerDNSCollector)

    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_work_with_fake_data(self, publish_mock):
        patch_communicate = patch('subprocess.Popen.communicate',
                                  Mock(return_value=(
                                    self.getFixture(
                                        'pdns_control-2.9.22.6-1.el6-A'
                                        ).getvalue(),
                                    '')))

        patch_communicate.start()
        self.collector.collect()
        patch_communicate.stop()

        self.assertPublishedMany(publish_mock, {})

        patch_communicate = patch('subprocess.Popen.communicate',
                                  Mock(return_value=(
                self.getFixture('pdns_control-2.9.22.6-1.el6-B').getvalue(),
                '')))

        patch_communicate.start()
        self.collector.collect()
        patch_communicate.stop()

        metrics = {
            'corrupt-packets': 1.0,
            'deferred-cache-inserts': 2.0,
            'deferred-cache-lookup': 3.0,
            'latency': 4.0,
            'packetcache-hit': 5.0,
            'packetcache-miss': 6.0,
            'packetcache-size': 7.0,
            'qsize-q': 8.0,
            'query-cache-hit': 9.0,
            'query-cache-miss': 10.0,
            'recursing-answers': 11.0,
            'recursing-questions': 12.0,
            'servfail-packets': 13.0,
            'tcp-answers': 14.0,
            'tcp-queries': 15.0,
            'timedout-packets': 16.0,
            'udp-answers': 17.0,
            'udp-queries': 18.0,
            'udp4-answers': 19.0,
            'udp4-queries': 20.0,
            'udp6-answers': 21.0,
            'udp6-queries': 22.0,
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

################################################################################
if __name__ == "__main__":
    unittest.main()
