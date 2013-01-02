#!/usr/bin/python
# coding=utf-8
################################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import Mock
from mock import patch

from diamond.collector import Collector
from ups import UPSCollector

################################################################################


class TestUPSCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('UPSCollector', {
            'interval': 10,
            'bin': 'true',
            'use_sudo': False,
        })

        self.collector = UPSCollector(config, None)

    def test_import(self):
        self.assertTrue(UPSCollector)

    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data_cp550slg(self, publish_mock):
        patch_listdir = patch('os.listdir', Mock(return_value=['sda']))
        patch_communicate = patch('subprocess.Popen.communicate',
                                  Mock(return_value=(
                                    self.getFixture('cp550slg').getvalue(),
                                    '')))
        patch_listdir.start()
        patch_communicate.start()
        self.collector.collect()
        patch_listdir.stop()
        patch_communicate.stop()

        metrics = {
            'battery.charge.charge': 100.0,
            'battery.charge.low': 10.0,
            'battery.charge.warning': 20.0,
            'battery.runtime.runtime': 960.0,
            'battery.runtime.low': 300.0,
            'battery.voltage.voltage': 4.9,
            'battery.voltage.nominal': 12.0,
            'driver.parameter.pollfreq': 30.0,
            'driver.parameter.pollinterval': 2.0,
            'driver.version.internal': 0.34,
            'input.transfer.high': 0.0,
            'input.transfer.low': 0.0,
            'input.voltage.voltage': 121.0,
            'input.voltage.nominal': 120.0,
            'output.voltage.voltage': 120.0,
            'ups.delay.shutdown': 20.0,
            'ups.delay.start': 30.0,
            'ups.load.load': 46.0,
            'ups.productid.productid': 501.0,
            'ups.realpower.nominal': 330.0,
            'ups.timer.shutdown': -60.0,
            'ups.timer.start': 0.0,
            'ups.vendorid.vendorid': 764.0,
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

################################################################################
if __name__ == "__main__":
    unittest.main()
