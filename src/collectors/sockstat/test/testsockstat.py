#!/usr/bin/python
################################################################################

from test import *

from diamond.collector import Collector
from sockstat import SockstatCollector

################################################################################

class TestSockstatCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('SockstatCollector', {
            'interval': 10
        })

        self.collector = SockstatCollector(config, None)

    @patch('__builtin__.open')
    @patch('os.access', Mock(return_value=True))

    @patch.object(Collector, 'publish')
    def test_should_open_proc_net_sockstat(self, publish_mock, open_mock):
        open_mock.return_value = StringIO('')
        self.collector.collect()
        open_mock.assert_called_once_with('/proc/net/sockstat')

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        SockstatCollector.PROC = self.getFixturePath('proc_net_sockstat')
        self.collector.collect()

        metrics = {
            'used'       : 118,
            'tcp_inuse'  : 10,
            'tcp_orphan' : 0,
            'tcp_tw'     : 1,
            'tcp_alloc'  : 13,
            'tcp_mem'    : 1,
            'udp_inuse'  : 0,
            'udp_mem'    : 0
        }
        
        self.setDocExample(self.collector.__class__.__name__, metrics)
        self.assertPublishedMany(publish_mock, metrics)

################################################################################
if __name__ == "__main__":
    unittest.main()
