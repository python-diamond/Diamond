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
except ImportError:
    from StringIO import StringIO

from diamond.collector import Collector
from network import NetworkCollector

################################################################################


class TestNetworkCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('NetworkCollector', {
            'interfaces': ['eth', 'em', 'bond', 'veth', 'br-lxc'],
            'interval':  10,
            'byte_unit': ['bit', 'megabit', 'megabyte'],
        })

        self.collector = NetworkCollector(config, None)

    def test_import(self):
        self.assertTrue(NetworkCollector)

    @patch('__builtin__.open')
    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_open_proc_net_dev(self, publish_mock, open_mock):
        open_mock.return_value = StringIO('')
        self.collector.collect()
        open_mock.assert_called_once_with('/proc/net/dev')

    @patch.object(Collector, 'publish')
    def test_should_work_with_virtual_interfaces_and_bridges(self,
                                                             publish_mock):
        NetworkCollector.PROC = self.getFixturePath('proc_net_dev_1')
        self.collector.collect()

        self.assertPublishedMany(publish_mock, {})

        NetworkCollector.PROC = self.getFixturePath('proc_net_dev_2')
        self.collector.collect()

        metrics = {
            'eth0.rx_megabyte': (2.504, 2),
            'eth0.tx_megabyte': (4.707, 2),
            'eth1.rx_megabyte': (0.0, 2),
            'eth1.tx_megabyte': (0.0, 2),
            'em2.rx_megabyte': (2.504, 2),
            'em2.tx_megabyte': (4.707, 2),
            'bond3.rx_megabyte': (2.504, 2),
            'bond3.tx_megabyte': (4.707, 2),
            'vethmR3i5e.tx_megabyte': (0.223, 2),
            'vethmR3i5e.rx_megabyte': (0.033, 2),
            'br-lxc-247.tx_megabyte': (0.307, 2),
            'br-lxc-247.rx_megabyte': (0.032, 2)
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        NetworkCollector.PROC = self.getFixturePath('proc_net_dev_1')
        self.collector.collect()

        self.assertPublishedMany(publish_mock, {})

        NetworkCollector.PROC = self.getFixturePath('proc_net_dev_2')
        self.collector.collect()

        metrics = {
            'eth0.rx_megabyte': (2.504, 2),
            'eth0.tx_megabyte': (4.707, 2),
            'eth1.rx_megabyte': (0.0, 2),
            'eth1.tx_megabyte': (0.0, 2),
            'em2.rx_megabyte': (2.504, 2),
            'em2.tx_megabyte': (4.707, 2),
            'bond3.rx_megabyte': (2.504, 2),
            'bond3.tx_megabyte': (4.707, 2)
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

    # Named test_z_* to run after test_should_open_proc_net_dev
    @patch.object(Collector, 'publish')
    def test_z_issue_208_a(self, publish_mock):
        NetworkCollector.PROC = self.getFixturePath('208-a_1')
        self.collector.collect()

        self.assertPublishedMany(publish_mock, {})

        NetworkCollector.PROC = self.getFixturePath('208-a_2')
        self.collector.collect()

        metrics = {
            'bond0.rx_bit': 2687979419428.0,
            'bond0.rx_compressed': 0.0,
            'bond0.rx_drop': 0.0,
            'bond0.rx_errors': 0.0,
            'bond0.rx_fifo': 0.0,
            'bond0.rx_frame': 0.0,
            'bond0.rx_multicast': 8481087.9,
            'bond0.rx_packets': 264585067.9,
            'bond0.tx_bit': 1569889402921.6,
            'bond0.tx_compressed': 0.0,
            'bond0.tx_drop': 0.0,
            'bond0.tx_errors': 0.0,
            'bond0.tx_fifo': 0.0,
            'bond0.tx_frame': 0.0,
            'bond0.tx_multicast': 0.0,
            'bond0.tx_packets': 200109891.6,
            'bond1.rx_bit': 16933606875970.4,
            'bond1.rx_compressed': 0.0,
            'bond1.rx_drop': 0.0,
            'bond1.rx_errors': 0.0,
            'bond1.rx_fifo': 0.0,
            'bond1.rx_frame': 0.0,
            'bond1.rx_multicast': 7.8,
            'bond1.rx_packets': 2419703159.9,
            'bond1.tx_bit': 17842573410005.6,
            'bond1.tx_compressed': 0.0,
            'bond1.tx_drop': 0.0,
            'bond1.tx_errors': 0.0,
            'bond1.tx_fifo': 0.0,
            'bond1.tx_frame': 0.0,
            'bond1.tx_multicast': 0.0,
            'bond1.tx_packets': 2654259261.0,
            'em1.rx_bit': 2687881969344.8,
            'em1.rx_compressed': 0.0,
            'em1.rx_drop': 0.0,
            'em1.rx_errors': 0.0,
            'em1.rx_fifo': 0.0,
            'em1.rx_frame': 0.0,
            'em1.rx_multicast': 8471878.8,
            'em1.rx_packets': 264382058.1,
            'em1.tx_bit': 1569889402921.6,
            'em1.tx_compressed': 0.0,
            'em1.tx_drop': 0.0,
            'em1.tx_errors': 0.0,
            'em1.tx_fifo': 0.0,
            'em1.tx_frame': 0.0,
            'em1.tx_multicast': 0.0,
            'em1.tx_packets': 200109891.6,
            'em2.rx_bit': 97450083.2,
            'em2.rx_compressed': 0.0,
            'em2.rx_drop': 0.0,
            'em2.rx_errors': 0.0,
            'em2.rx_fifo': 0.0,
            'em2.rx_frame': 0.0,
            'em2.rx_multicast': 9209.1,
            'em2.rx_packets': 203009.8,
            'em2.tx_bit': 0,
            'em2.tx_compressed': 0.0,
            'em2.tx_drop': 0.0,
            'em2.tx_errors': 0.0,
            'em2.tx_fifo': 0.0,
            'em2.tx_frame': 0.0,
            'em2.tx_multicast': 0.0,
            'em2.tx_packets': 0.0,
            'em3.rx_bit': 514398.4,
            'em3.rx_compressed': 0.0,
            'em3.rx_drop': 0.0,
            'em3.rx_errors': 0.0,
            'em3.rx_fifo': 0.0,
            'em3.rx_frame': 0.0,
            'em3.rx_multicast': 0.0,
            'em3.rx_packets': 1071.6,
            'em3.tx_bit': 0.0,
            'em3.tx_compressed': 0.0,
            'em3.tx_drop': 0.0,
            'em3.tx_errors': 0.0,
            'em3.tx_fifo': 0.0,
            'em3.tx_frame': 0.0,
            'em3.tx_multicast': 0.0,
            'em3.tx_packets': 0.0,
            'em4.rx_bit': 16933606361572.0,
            'em4.rx_compressed': 0.0,
            'em4.rx_drop': 0.0,
            'em4.rx_errors': 0.0,
            'em4.rx_fifo': 0.0,
            'em4.rx_frame': 0.0,
            'em4.rx_multicast': 7.8,
            'em4.rx_packets': 2419702088.3,
            'em4.tx_bit': 17842573410005.6,
            'em4.tx_compressed': 0.0,
            'em4.tx_drop': 0.0,
            'em4.tx_errors': 0.0,
            'em4.tx_fifo': 0.0,
            'em4.tx_frame': 0.0,
            'em4.tx_multicast': 0.0,
            'em4.tx_packets': 2654259261.0,
        }

        self.assertPublishedMany(publish_mock, metrics)

    # Named test_z_* to run after test_should_open_proc_net_dev
    @patch.object(Collector, 'publish')
    def test_z_issue_208_b(self, publish_mock):
        NetworkCollector.PROC = self.getFixturePath('208-b_1')
        self.collector.collect()

        self.assertPublishedMany(publish_mock, {})

        NetworkCollector.PROC = self.getFixturePath('208-b_2')
        self.collector.collect()

        metrics = {
            'bond0.rx_bit': 12754357408.8,
            'bond0.rx_compressed': 0.0,
            'bond0.rx_drop': 0.0,
            'bond0.rx_errors': 0.0,
            'bond0.rx_fifo': 0.0,
            'bond0.rx_frame': 0.0,
            'bond0.rx_multicast': 8483853.6,
            'bond0.rx_packets': 13753449.5,
            'bond0.tx_bit': 51593345279.2,
            'bond0.tx_compressed': 0.0,
            'bond0.tx_drop': 0.0,
            'bond0.tx_errors': 0.0,
            'bond0.tx_fifo': 0.0,
            'bond0.tx_frame': 0.0,
            'bond0.tx_multicast': 0.0,
            'bond0.tx_packets': 58635426.6,
            'bond1.rx_bit': 48298217736175.2,
            'bond1.rx_compressed': 0.0,
            'bond1.rx_drop': 0.0,
            'bond1.rx_errors': 0.0,
            'bond1.rx_fifo': 473.8,
            'bond1.rx_frame': 0.0,
            'bond1.rx_multicast': 2.9,
            'bond1.rx_packets': 4869871086.2,
            'bond1.tx_bit': 23149038213964.0,
            'bond1.tx_compressed': 0.0,
            'bond1.tx_drop': 0.0,
            'bond1.tx_errors': 0.0,
            'bond1.tx_fifo': 0.0,
            'bond1.tx_frame': 0.0,
            'bond1.tx_multicast': 0.0,
            'bond1.tx_packets': 2971941537.3,
            'em1.rx_bit': 12657057999.2,
            'em1.rx_compressed': 0.0,
            'em1.rx_drop': 0.0,
            'em1.rx_errors': 0.0,
            'em1.rx_fifo': 0.0,
            'em1.rx_frame': 0.0,
            'em1.rx_multicast': 8474644.4,
            'em1.rx_packets': 13550781.5,
            'em1.tx_bit': 51593345279.2,
            'em1.tx_compressed': 0.0,
            'em1.tx_drop': 0.0,
            'em1.tx_errors': 0.0,
            'em1.tx_fifo': 0.0,
            'em1.tx_frame': 0.0,
            'em1.tx_multicast': 0.0,
            'em1.tx_packets': 58635426.6,
            'em2.rx_bit': 97299409.6,
            'em2.rx_compressed': 0.0,
            'em2.rx_drop': 0.0,
            'em2.rx_errors': 0.0,
            'em2.rx_fifo': 0.0,
            'em2.rx_frame': 0.0,
            'em2.rx_multicast': 9209.2,
            'em2.rx_packets': 202668.0,
            'em2.tx_bit': 0,
            'em2.tx_compressed': 0.0,
            'em2.tx_drop': 0.0,
            'em2.tx_errors': 0.0,
            'em2.tx_fifo': 0.0,
            'em2.tx_frame': 0.0,
            'em2.tx_multicast': 0.0,
            'em2.tx_packets': 0.0,
            'em3.rx_bit': 48298184648012.0,
            'em3.rx_compressed': 0.0,
            'em3.rx_drop': 0.0,
            'em3.rx_errors': 0.0,
            'em3.rx_fifo': 473.8,
            'em3.rx_frame': 0.0,
            'em3.rx_multicast': 2.9,
            'em3.rx_packets': 4869866440.5,
            'em3.tx_bit': 23149038213964.0,
            'em3.tx_compressed': 0.0,
            'em3.tx_drop': 0.0,
            'em3.tx_errors': 0.0,
            'em3.tx_fifo': 0.0,
            'em3.tx_frame': 0.0,
            'em3.tx_multicast': 0.0,
            'em3.tx_packets': 2971941537.3,
            'em4.rx_bit': 33088163.2,
            'em4.rx_compressed': 0.0,
            'em4.rx_drop': 0.0,
            'em4.rx_errors': 0.0,
            'em4.rx_fifo': 0.0,
            'em4.rx_frame': 0.0,
            'em4.rx_multicast': 0.0,
            'em4.rx_packets': 4645.7,
            'em4.tx_bit': 0,
            'em4.tx_compressed': 0.0,
            'em4.tx_drop': 0.0,
            'em4.tx_errors': 0.0,
            'em4.tx_fifo': 0.0,
            'em4.tx_frame': 0.0,
            'em4.tx_multicast': 0.0,
            'em4.tx_packets': 0.0,
        }

        self.assertPublishedMany(publish_mock, metrics)

################################################################################
if __name__ == "__main__":
    unittest.main()
