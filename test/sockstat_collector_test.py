#!/usr/bin/python
################################################################################

from common import *

from diamond.collector import Collector
from sockstat_collector import SockstatCollector

################################################################################

class TestSockstatCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('SockstatCollector', {
            'interval': 10
        })

        self.collector = SockstatCollector(config, None)

    @patch('__builtin__.open')
    @patch.object(Collector, 'publish')
    def test_should_open_proc_net_sockstat(self, publish_mock, open_mock):
        open_mock.return_value.__iter__.return_value = iter([])
        self.collector.collect()
        open_mock.assert_called_once_with('/proc/net/sockstat', 'r')

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        SockstatCollector.PROC = get_fixture_path('proc_net_sockstat')
        self.collector.collect()

        self.assertPublishedMany(publish_mock, {
            'used'       : 118,
            'tcp_inuse'  : 10,
            'tcp_orphan' : 0,
            'tcp_tw'     : 1,
            'tcp_alloc'  : 13,
            'tcp_mem'    : 1,
            'udp_inuse'  : 0,
            'udp_mem'    : 0
        })

################################################################################
if __name__ == "__main__":
    unittest.main()
