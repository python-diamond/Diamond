#!/usr/bin/python
################################################################################

from common import *

from diamond.collector import Collector
from network_collector import NetworkCollector

################################################################################

class TestNetworkCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('NetworkCollector', {
            'interval': 10,
            'interfaces' : [ 'lo', 'eth0' ]
        })

        self.collector = NetworkCollector(config, None)
    
    @patch('__builtin__.open')
    @patch.object(Collector, 'publish')
    def test_should_open_proc_fs(self, publish_mock, open_mock):
        open_mock.return_value.__iter__.return_value = iter([])
        self.collector.collect()
        open_mock.assert_called_once_with('/proc/net/dev', 'r')

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        NetworkCollector.PROC = get_fixture_path('proc_net_dev_1')
        self.collector.collect()

        self.assertPublishedMany(publish_mock, {
            'lo.rx_bytes'   : 0.0,
            'lo.tx_bytes'   : 0.0,
            'eth0.rx_bytes' : 0.0,
            'eth0.tx_bytes' : 0.0
        })
        publish_mock.reset_mock()

        NetworkCollector.PROC = get_fixture_path('proc_net_dev_2')
        self.collector.collect()

        self.assertPublishedMany(publish_mock, {
            'lo.rx_bytes'   : 0.0,
            'lo.tx_bytes'   : 0.0,
            'eth0.rx_bytes' : 33.2,
            'eth0.tx_bytes' : 317.4
        })
        publish_mock.reset_mock()
        

################################################################################
if __name__ == "__main__":
    unittest.main()
