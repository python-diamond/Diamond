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

from tcp import TCPCollector

################################################################################


class TestTCPCollector(CollectorTestCase):
    def setUp(self, allowed_names=None):
        if not allowed_names:
            allowed_names = []
        config = get_collector_config('TCPCollector', {
            'allowed_names': allowed_names,
            'interval': 1
        })
        self.collector = TCPCollector(config, None)

    def test_import(self):
        self.assertTrue(TCPCollector)

    @patch('os.access', Mock(return_value=True))
    @patch('__builtin__.open')
    @patch('diamond.collector.Collector.publish')
    def test_should_open_proc_net_netstat(self, publish_mock, open_mock):
        TCPCollector.PROC = ['/proc/net/netstat']
        open_mock.return_value = StringIO('')
        self.collector.collect()
        open_mock.assert_called_once_with('/proc/net/netstat')

    @patch('os.access', Mock(return_value=True))
    @patch('__builtin__.open')
    @patch('diamond.collector.Collector.publish')
    def test_should_work_with_synthetic_data(self, publish_mock, open_mock):
        TCPCollector.PROC = ['/proc/net/netstat']
        self.setUp(['A', 'C'])
        open_mock.return_value = StringIO('''
TcpExt: A B C
TcpExt: 0 0 0
'''.strip())

        self.collector.collect()
        self.assertPublishedMany(publish_mock, {})

        open_mock.return_value = StringIO('''
TcpExt: A B C
TcpExt: 0 1 2
'''.strip())

        self.collector.collect()

        self.assertEqual(len(publish_mock.call_args_list), 2)

        metrics = {
            'A': 0,
            'C': 2,
        }

        self.assertPublishedMany(publish_mock, metrics)

    @patch('diamond.collector.Collector.publish')
    def test_should_work_with_real_data(self, publish_mock):
        self.setUp(['ListenOverflows', 'ListenDrops', 'TCPLoss', 'TCPTimeouts'])

        TCPCollector.PROC = [self.getFixturePath('proc_net_netstat_1')]
        self.collector.collect()
        self.assertPublishedMany(publish_mock, {})

        TCPCollector.PROC = [self.getFixturePath('proc_net_netstat_2')]
        self.collector.collect()

        metrics = {
            'ListenOverflows': 0,
            'ListenDrops': 0,
            'TCPLoss': 188,
            'TCPTimeouts': 15265
        }

        self.assertPublishedMany(publish_mock, metrics)

    @patch('diamond.collector.Collector.publish')
    def test_should_work_with_all_data(self, publish_mock):
        self.setUp([])

        TCPCollector.PROC = [
            self.getFixturePath('proc_net_netstat_1'),
            self.getFixturePath('proc_net_snmp_1'),
            ]
        self.collector.collect()
        self.assertPublishedMany(publish_mock, {})

        TCPCollector.PROC = [
            self.getFixturePath('proc_net_netstat_2'),
            self.getFixturePath('proc_net_snmp_2'),
            ]
        self.collector.collect()

        metrics = {
            'TCPMD5Unexpected':             0.0,
            'ArpFilter':                    0.0,
            'TCPBacklogDrop':               0.0,
            'TCPDSACKRecv':                 1580.0,
            'TCPDSACKIgnoredOld':           292.0,
            'MaxConn':                      (-1.0),
            'RcvPruned':                    0.0,
            'TCPSackMerged':                1121.0,
            'OutOfWindowIcmps':             10.0,
            'TCPDeferAcceptDrop':           0.0,
            'TCPLossUndo':                  6538.0,
            'TCPHPHitsToUser':              5667.0,
            'TCPTimeouts':                  15265.0,
            'TCPForwardRetrans':            41.0,
            'TCPTSReorder':                 0.0,
            'RtoMin':                       0.0,
            'TCPAbortOnData':               143.0,
            'TCPFullUndo':                  0.0,
            'TCPSackRecoveryFail':          13.0,
            'InErrs':                       0.0,
            'TCPAbortOnClose':              38916.0,
            'TCPAbortOnTimeout':            68.0,
            'TCPFACKReorder':               0.0,
            'LockDroppedIcmps':             4.0,
            'RtoMax':                       0.0,
            'TCPSchedulerFailed':           0.0,
            'EstabResets':                  0.0,
            'DelayedACKs':                  125491.0,
            'TCPSACKReneging':              0.0,
            'PruneCalled':                  0.0,
            'OutRsts':                      0.0,
            'TCPRenoRecoveryFail':          0.0,
            'TCPSackShifted':               2356.0,
            'DelayedACKLocked':             144.0,
            'TCPHPHits':                    10361792.0,
            'EmbryonicRsts':                0.0,
            'TCPLossFailures':              7.0,
            'TWKilled':                     0.0,
            'TCPSACKDiscard':               0.0,
            'TCPAbortFailed':               0.0,
            'TCPSackRecovery':              364.0,
            'TCPDirectCopyFromBacklog':     35660.0,
            'TCPFastRetrans':               1184.0,
            'TCPPartialUndo':               0.0,
            'TCPMinTTLDrop':                0.0,
            'SyncookiesSent':               0.0,
            'OutSegs':                      0.0,
            'TCPSackShiftFallback':         3091.0,
            'RetransSegs':                  0.0,
            'IPReversePathFilter':          0.0,
            'TCPRcvCollapsed':              0.0,
            'TCPDSACKUndo':                 2448.0,
            'SyncookiesFailed':             9.0,
            'TCPSACKReorder':               0.0,
            'TCPDSACKOldSent':              10175.0,
            'TCPAbortOnLinger':             0.0,
            'TCPSpuriousRTOs':              9.0,
            'TCPRenoRecovery':              0.0,
            'TCPPrequeued':                 114232.0,
            'TCPLostRetransmit':            7.0,
            'TCPLoss':                      188.0,
            'TCPHPAcks':                    12673896.0,
            'TCPDSACKOfoRecv':              0.0,
            'TWRecycled':                   0.0,
            'TCPRenoFailures':              0.0,
            'OfoPruned':                    0.0,
            'TCPMD5NotFound':               0.0,
            'ActiveOpens':                  0.0,
            'TCPDSACKIgnoredNoUndo':        1025.0,
            'TCPPrequeueDropped':           0.0,
            'RtoAlgorithm':                 0.0,
            'TCPAbortOnMemory':             0.0,
            'TCPTimeWaitOverflow':          0.0,
            'TCPAbortOnSyn':                0.0,
            'TCPDirectCopyFromPrequeue':    19340531.0,
            'DelayedACKLost':               10118.0,
            'PassiveOpens':                 0.0,
            'InSegs':                       1.0,
            'PAWSPassive':                  0.0,
            'TCPRenoReorder':               0.0,
            'CurrEstab':                    3.0,
            'TW':                           89479.0,
            'AttemptFails':                 0.0,
            'PAWSActive':                   0.0,
            'ListenDrops':                  0.0,
            'SyncookiesRecv':               0.0,
            'TCPDSACKOfoSent':              0.0,
            'TCPSlowStartRetrans':          2540.0,
            'TCPMemoryPressures':           0.0,
            'PAWSEstab':                    0.0,
            'TCPSackFailures':              502.0,
            'ListenOverflows':              0.0,
            'TCPPureAcks':                  1003528.0,
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

################################################################################
if __name__ == "__main__":
    unittest.main()
