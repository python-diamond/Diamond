#!/usr/bin/python
################################################################################

from common import *
from collectors.tcp import TCPCollector

################################################################################

class TestTCPCollector(unittest.TestCase):
    def setUp(self):
        self.collector = TCPCollector(get_collector_config(), None)

    @patch('__builtin__.open')
    @patch.object(diamond.collector.Collector, 'publish')
    def test_should_open_proc_fs(self, publish_mock, open_mock):
        open_mock.return_value.__iter__.return_value = iter([])

        self.collector.collect()

        open_mock.assert_called_once_with('/proc/net/netstat', 'r')

    @patch('__builtin__.open')
    @patch.object(diamond.collector.Collector, 'publish')
    def test_should_work_with_empty_data(self, publish_mock, open_mock):
        open_mock.return_value.__iter__.return_value = iter([])

        self.collector.collect()

        self.assertEqual(len(publish_mock.call_args_list), 0)

    @patch('__builtin__.open')
    @patch.object(diamond.collector.Collector, 'publish')
    def test_should_work_with_synthetic_data(self, publish_mock, open_mock):
        open_mock.return_value.__iter__.return_value = iter([
            'TcpExt: A B C',
            'TcpExt: 0 1 2'
        ])

        self.collector.collect()

        self.assertEqual(len(publish_mock.call_args_list), 3)
        self.assertEqual(publish_mock.call_args_list, [
            call('A', '0', 0),
            call('B', '1', 0),
            call('C', '2', 0)
        ])

    @patch.object(diamond.collector.Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        TCPCollector.PROC = get_fixture_path('proc_net_netstat')

        self.collector.collect()

        def check_specific_pair(key, expected_value):
            calls = filter(lambda x: x[0][0] == key, publish_mock.call_args_list)
            self.assertEqual(len(calls), 1)
            self.assertEqual(calls[0][0][1], str(expected_value))

        check_specific_pair('TCPLossUndo', 6538)
        check_specific_pair('TCPDSACKRecv', 1580)
        check_specific_pair('TCPHPHits', 10361792)
        check_specific_pair('TCPSackShiftFallback', 3091)
        check_specific_pair('TCPAbortOnData', 143)

################################################################################
if __name__ == "__main__":
    unittest.main()
