#!/usr/bin/python
# coding=utf-8
################################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import Mock
from mock import patch

try:
    from cStringIO import StringIO
    StringIO  # workaround for pyflakes issue #13
except ImportError:
    from StringIO import StringIO

from diamond.collector import Collector
from interrupt import InterruptCollector

################################################################################


class TestInterruptCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('InterruptCollector', {
            'interval': 1
        })

        self.collector = InterruptCollector(config, None)

    def test_import(self):
        self.assertTrue(InterruptCollector)

    @patch('__builtin__.open')
    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_open_proc_stat(self, publish_mock, open_mock):
        open_mock.return_value = StringIO('')
        self.collector.collect()
        open_mock.assert_called_once_with('/proc/interrupts', 'r')

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data_24_core(self, publish_mock):
        InterruptCollector.PROC = self.getFixturePath('interrupts_24_core_1')
        self.collector.collect()

        self.assertPublishedMany(publish_mock, {})

        InterruptCollector.PROC = self.getFixturePath('interrupts_24_core_2')
        self.collector.collect()

        metrics = {
            'IO-APIC-edge.timer.0.CPU0': 318660.000000,
            'IO-APIC-edge.timer.0.total': 318660.000000,
            'PCI-MSI-X.eth3-rx-1.51.CPU6': 293.000000,
            'PCI-MSI-X.eth3-rx-1.51.CPU7': 330.000000,
            'PCI-MSI-X.eth3-rx-1.51.CPU9': 286.000000,
            'PCI-MSI-X.eth3-rx-1.51.total': 909.000000,
            'PCI-MSI-X.eth3-rx-2.59.CPU21': 98790.000000,
            'PCI-MSI-X.eth3-rx-2.59.total': 98790.000000,
            'PCI-MSI-X.eth3-rx-3.67.CPU7': 743.000000,
            'PCI-MSI-X.eth3-rx-3.67.CPU9': 378.000000,
            'PCI-MSI-X.eth3-rx-3.67.total': 1121.000000,
            'PCI-MSI-X.eth3-tx-0.75.CPU23': 304345.000000,
            'PCI-MSI-X.eth3-tx-0.75.total': 304345.000000,
            'IO-APIC-level_3w-sas.CPU6': 301014.000000,
            'IO-APIC-level_3w-sas.total': 301014.000000,
            'PCI-MSI-X_eth2-rx-0.CPU20': 20570.000000,
            'PCI-MSI-X_eth2-rx-0.total': 20570.000000,
            'PCI-MSI-X_eth2-rx-1.CPU6': 94.000000,
            'PCI-MSI-X_eth2-rx-1.CPU7': 15.000000,
            'PCI-MSI-X_eth2-rx-1.CPU9': 50.000000,
            'PCI-MSI-X_eth2-rx-1.total': 159.000000,
            'PCI-MSI-X_eth2-rx-2.CPU17': 159.000000,
            'PCI-MSI-X_eth2-rx-2.total': 159.000000,
            'PCI-MSI-X_eth2-rx-3.CPU8': 159.000000,
            'PCI-MSI-X_eth2-rx-3.total': 159.000000,
            'PCI-MSI-X_eth2-tx-0.CPU16': 159.000000,
            'PCI-MSI-X_eth2-tx-0.total': 159.000000,
            'PCI-MSI_eth0.CPU18': 10397.000000,
            'PCI-MSI_eth0.total': 10397.000000,
            'PCI-MSI-X_eth3-rx-0.CPU22': 224074.000000,
            'PCI-MSI-X_eth3-rx-0.total': 224074.000000,
            'PCI-MSI_eth1.CPU19': 10386.000000,
            'PCI-MSI_eth1.total': 10386.000000,
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data_kvm(self, publish_mock):
        InterruptCollector.PROC = self.getFixturePath('interrupts_kvm_1')
        self.collector.collect()

        self.assertPublishedMany(publish_mock, {})

        InterruptCollector.PROC = self.getFixturePath('interrupts_kvm_2')
        self.collector.collect()

        self.assertPublishedMany(publish_mock, {
            'IO-APIC-edge.timer.0.CPU0': 279023.000000,
            'IO-APIC-edge.timer.0.total': 279023.000000,
            'IO-APIC-level.virtio0-virtio1.10.CPU0': 15068.000000,
            'IO-APIC-level.virtio0-virtio1.10.total': 15068.000000,
            'LOC.CPU0': 278993.000000,
            'LOC.CPU1': 279000.000000,
            'LOC.total': 557993.000000,
        })

################################################################################
if __name__ == "__main__":
    unittest.main()
