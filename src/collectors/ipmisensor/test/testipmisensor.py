#!/usr/bin/python
# coding=utf-8
################################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import Mock
from mock import patch

from diamond.collector import Collector
from ipmisensor import IPMISensorCollector

################################################################################


class TestIPMISensorCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('IPMISensorCollector', {
            'interval': 10,
            'bin': 'true',
            'use_sudo': False
        })

        self.collector = IPMISensorCollector(config, None)

    def test_import(self):
        self.assertTrue(IPMISensorCollector)

    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        patch_communicate = patch('subprocess.Popen.communicate',
                                   Mock(return_value=(
                                    self.getFixture('ipmitool.out').getvalue(),
                                    '')))

        patch_communicate.start()
        self.collector.collect()
        patch_communicate.stop()

        metrics = {
            'System.Temp': 32.000000,
            'CPU1.Vcore': 1.080000,
            'CPU2.Vcore': 1.000000,
            'CPU1.VTT': 1.120000,
            'CPU2.VTT': 1.176000,
            'CPU1.DIMM': 1.512000,
            'CPU2.DIMM': 1.512000,
            '+1_5V': 1.512000,
            '+1_8V': 1.824000,
            '+5V': 4.992000,
            '+12V': 12.031000,
            '+1_1V': 1.112000,
            '+3_3V': 3.288000,
            '+3_3VSB': 3.240000,
            'VBAT': 3.240000,
            'Fan1': 4185.000000,
            'Fan2': 4185.000000,
            'Fan3': 4185.000000,
            'Fan7': 3915.000000,
            'Fan8': 3915.000000,
            'Intrusion': 0.000000,
            'PS.Status': 0.000000,
            'P1-DIMM1A.Temp': 41.000000,
            'P1-DIMM1B.Temp': 39.000000,
            'P1-DIMM2A.Temp': 38.000000,
            'P1-DIMM2B.Temp': 40.000000,
            'P1-DIMM3A.Temp': 37.000000,
            'P1-DIMM3B.Temp': 38.000000,
            'P2-DIMM1A.Temp': 39.000000,
            'P2-DIMM1B.Temp': 38.000000,
            'P2-DIMM2A.Temp': 39.000000,
            'P2-DIMM2B.Temp': 39.000000,
            'P2-DIMM3A.Temp': 39.000000,
            'P2-DIMM3B.Temp': 40.000000,
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

################################################################################
if __name__ == "__main__":
    unittest.main()
