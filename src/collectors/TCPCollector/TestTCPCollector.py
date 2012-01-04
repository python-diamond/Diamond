#!/usr/bin/python
################################################################################

from test import *

from diamond.collector import Collector
from TCPCollector import TCPCollector

################################################################################

class TestTCPCollector(CollectorTestCase):
    def setUp(self, allowed_names = []):
        config = get_collector_config('TCPCollector', {
            'allowed_names' : allowed_names
        })
        self.collector = TCPCollector(config, None)

    @patch('os.access', Mock(return_value=True))
    @patch('__builtin__.open')
    @patch.object(Collector, 'publish')
    def test_should_open_proc_net_netstat(self, publish_mock, open_mock):
        open_mock.return_value = StringIO('')
        self.collector.collect()
        open_mock.assert_called_once_with('/proc/net/netstat')

    @patch('__builtin__.open')
    @patch.object(Collector, 'publish')
    def test_should_work_with_synthetic_data(self, publish_mock, open_mock):
        self.setUp([ 'A', 'C' ])
        open_mock.return_value = StringIO('''
TcpExt: A B C
TcpExt: 0 1 2
'''.strip())

        self.collector.collect()

        self.assertEqual(len(publish_mock.call_args_list), 2)
        self.assertEqual(publish_mock.call_args_list, [
            (('A', '0', 0), {}),
            (('C', '2', 0), {})
        ])

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        self.setUp([ 'ListenOverflows', 'ListenDrops', 'TCPLoss', 'TCPTimeouts' ])
        TCPCollector.PROC = self.getFixturePath('proc_net_netstat')
        self.collector.collect()

        self.assertPublishedMany(publish_mock, {
            'ListenOverflows'  : 0,
            'ListenDrops'      : 0,
            'TCPLoss'          : 188,
            'TCPTimeouts'      : 15265
        })

################################################################################
if __name__ == "__main__":
    unittest.main()
