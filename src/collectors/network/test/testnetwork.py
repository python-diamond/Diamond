#!/usr/bin/python
# coding=utf-8
################################################################################

from test import *

from diamond.collector import Collector
from network import NetworkCollector

################################################################################


class TestNetworkCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('NetworkCollector', {
            'interval': 10,
        })

        self.collector = NetworkCollector(config, None)

    @patch('__builtin__.open')
    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_open_proc_net_dev(self, publish_mock, open_mock):
        open_mock.return_value = StringIO('')
        self.collector.collect()
        open_mock.assert_called_once_with('/proc/net/dev')

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
            'eth1.tx_megabyte': (0.0, 2)
        }

        self.setDocExample(self.collector.__class__.__name__, metrics)
        self.assertPublishedMany(publish_mock, metrics)


################################################################################
if __name__ == "__main__":
    unittest.main()
