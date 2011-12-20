#!/usr/bin/python
################################################################################

from common import *

from diamond.collector import Collector
from NetworkCollector import NetworkCollector

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
    def test_should_open_proc_net_dev(self, publish_mock, open_mock):
        open_mock.return_value = StringIO('')
        self.collector.collect()
        open_mock.assert_called_once_with('/proc/net/dev')

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        NetworkCollector.PROC = get_fixture_path('proc_net_dev_1')
        self.collector.collect()

        self.assertPublishedMany(publish_mock, {})

        NetworkCollector.PROC = get_fixture_path('proc_net_dev_2')
        self.collector.collect()

        self.assertPublishedMany(publish_mock, {
            'lo.rx_mbytes'   : (0.0, 2),
            'lo.tx_mbytes'   : (0.0, 2),
            'eth0.rx_mbytes' : (2.504, 2),
            'eth0.tx_mbytes' : (4.707, 2)
        })


################################################################################
if __name__ == "__main__":
    unittest.main()
