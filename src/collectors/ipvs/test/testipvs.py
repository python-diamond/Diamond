#!/usr/bin/python
# coding=utf-8
################################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import Mock
from mock import patch

from diamond.collector import Collector
from ipvs import IPVSCollector

################################################################################


class TestIPVSCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('IPVSCollector', {
            'interval': 10,
            'bin': 'true',
            'use_sudo': False
        })

        self.collector = IPVSCollector(config, None)

    def test_import(self):
        self.assertTrue(IPVSCollector)

    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        patch_communicate = patch('subprocess.Popen.communicate',
                                   Mock(return_value=(
                                    self.getFixture('ipvsadm').getvalue(),
                                    '')))

        patch_communicate.start()
        self.collector.collect()
        patch_communicate.stop()

        metrics = {
            "TCP_172_16_1_56:80.total.conns": 116,
            "TCP_172_16_1_56:443.total.conns": 59,
            "TCP_172_16_1_56:443.10_68_15_66:443.conns": 59,
            "TCP_172_16_1_56:443.10_68_15_66:443.outbytes": 216873,
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

################################################################################
if __name__ == "__main__":
    unittest.main()
