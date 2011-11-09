#!/usr/bin/python
################################################################################

from common import *

from diamond.collector import Collector
from tcp_collector import TCPCollector

################################################################################

class TestTCPCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('TCPCollector', {})
        self.collector = TCPCollector(config, None)

    @patch('__builtin__.open')
    @patch.object(Collector, 'publish')
    def test_should_open_proc_net_netstat(self, publish_mock, open_mock):
        open_mock.return_value = StringIO('')
        self.collector.collect()
        open_mock.assert_called_once_with('/proc/net/netstat')

    @patch('__builtin__.open')
    @patch.object(Collector, 'publish')
    def test_should_work_with_synthetic_data(self, publish_mock, open_mock):
        open_mock.return_value = StringIO('''
TcpExt: A B C
TcpExt: 0 1 2
'''.strip())

        self.collector.collect()

        self.assertEqual(len(publish_mock.call_args_list), 3)
        self.assertEqual(publish_mock.call_args_list, [
            call('A', '0', 0),
            call('B', '1', 0),
            call('C', '2', 0)
        ])

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        TCPCollector.PROC = get_fixture_path('proc_net_netstat')
        self.collector.collect()

        self.assertPublishedMany(publish_mock, {
            'TCPLossUndo'          : '6538',
            'TCPDSACKRecv'         : '1580',
            'TCPHPHits'            : '10361792',
            'TCPSackShiftFallback' : '3091',
            'TCPAbortOnData'       : '143'
        })

################################################################################
if __name__ == "__main__":
    unittest.main()
