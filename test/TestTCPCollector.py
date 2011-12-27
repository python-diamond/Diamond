#!/usr/bin/python
################################################################################

from common import *

from diamond.collector import Collector
from TCPCollector import TCPCollector

################################################################################

class TestTCPCollector(CollectorTestCase):
    def setUp(self, allowed_names = []):
        config = get_collector_config('TCPCollector', {
            'allowed_names' : allowed_names
        })
        self.collector = TCPCollector(config, None)

    @patch('__builtin__.open')
    @patch('os.access', Mock(return_value=True))

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
        self.setUp([ 'DelayedACKs', 'DelayedACKLocked', 'DelayedACKLost' ])
        TCPCollector.PROC = get_fixture_path('proc_net_netstat')
        self.collector.collect()

        self.assertPublishedMany(publish_mock, {
            'DelayedACKs'      : '125491',
            'DelayedACKLocked' : '144',
            'DelayedACKLost'   : '10118'
        })

################################################################################
if __name__ == "__main__":
    unittest.main()
