#!/usr/bin/python
# coding=utf-8
################################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import Mock
from mock import patch

from diamond.collector import Collector
from bind import BindCollector

################################################################################


class TestBindCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('BindCollector', {
            'interval': 10,
        })

        self.collector = BindCollector(config, None)

    def test_import(self):
        self.assertTrue(BindCollector)

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        patch_urlopen = patch('urllib2.urlopen', Mock(
            return_value=self.getFixture('bind.xml')))

        patch_urlopen.start()
        self.collector.collect()
        patch_urlopen.stop()

        metrics = {
            'view._default.resstat.Queryv4': 0.000000,
            'view._default.resstat.Queryv6': 0.000000,
            'view._default.resstat.Responsev4': 0.000000,
            'view._default.resstat.Responsev6': 0.000000,
            'view._default.resstat.NXDOMAIN': 0.000000,
            'view._default.resstat.SERVFAIL': 0.000000,
            'view._default.resstat.FORMERR': 0.000000,
            'view._default.resstat.OtherError': 0.000000,
            'view._default.resstat.EDNS0Fail': 0.000000,
            'view._default.resstat.Mismatch': 0.000000,
            'view._default.resstat.Truncated': 0.000000,
            'view._default.resstat.Lame': 0.000000,
            'view._default.resstat.Retry': 0.000000,
            'view._default.resstat.QueryAbort': 0.000000,
            'view._default.resstat.QuerySockFail': 0.000000,
            'view._default.resstat.QueryTimeout': 0.000000,
            'view._default.resstat.GlueFetchv4': 0.000000,
            'view._default.resstat.GlueFetchv6': 0.000000,
            'view._default.resstat.GlueFetchv4Fail': 0.000000,
            'view._default.resstat.GlueFetchv6Fail': 0.000000,
            'view._default.resstat.ValAttempt': 0.000000,
            'view._default.resstat.ValOk': 0.000000,
            'view._default.resstat.ValNegOk': 0.000000,
            'view._default.resstat.ValFail': 0.000000,
            'view._default.resstat.QryRTT10': 0.000000,
            'view._default.resstat.QryRTT100': 0.000000,
            'view._default.resstat.QryRTT500': 0.000000,
            'view._default.resstat.QryRTT800': 0.000000,
            'view._default.resstat.QryRTT1600': 0.000000,
            'view._default.resstat.QryRTT1600+': 0.000000,
            'requests.QUERY': 0.000000,
            'queries.A': 0.000000,
            'nsstat.Requestv4': 0.000000,
            'nsstat.Requestv6': 0.000000,
            'nsstat.ReqEdns0': 0.000000,
            'nsstat.ReqBadEDNSVer': 0.000000,
            'nsstat.ReqTSIG': 0.000000,
            'nsstat.ReqSIG0': 0.000000,
            'nsstat.ReqBadSIG': 0.000000,
            'nsstat.ReqTCP': 0.000000,
            'nsstat.AuthQryRej': 0.000000,
            'nsstat.RecQryRej': 0.000000,
            'nsstat.XfrRej': 0.000000,
            'nsstat.UpdateRej': 0.000000,
            'nsstat.Response': 0.000000,
            'nsstat.TruncatedResp': 0.000000,
            'nsstat.RespEDNS0': 0.000000,
            'nsstat.RespTSIG': 0.000000,
            'nsstat.RespSIG0': 0.000000,
            'nsstat.QrySuccess': 0.000000,
            'nsstat.QryAuthAns': 0.000000,
            'nsstat.QryNoauthAns': 0.000000,
            'nsstat.QryReferral': 0.000000,
            'nsstat.QryNxrrset': 0.000000,
            'nsstat.QrySERVFAIL': 0.000000,
            'nsstat.QryFORMERR': 0.000000,
            'nsstat.QryNXDOMAIN': 0.000000,
            'nsstat.QryRecursion': 0.000000,
            'nsstat.QryDuplicate': 0.000000,
            'nsstat.QryDropped': 0.000000,
            'nsstat.QryFailure': 0.000000,
            'nsstat.XfrReqDone': 0.000000,
            'nsstat.UpdateReqFwd': 0.000000,
            'nsstat.UpdateRespFwd': 0.000000,
            'nsstat.UpdateFwdFail': 0.000000,
            'nsstat.UpdateDone': 0.000000,
            'nsstat.UpdateFail': 0.000000,
            'nsstat.UpdateBadPrereq': 0.000000,
            'zonestat.NotifyOutv4': 0.000000,
            'zonestat.NotifyOutv6': 0.000000,
            'zonestat.NotifyInv4': 0.000000,
            'zonestat.NotifyInv6': 0.000000,
            'zonestat.NotifyRej': 0.000000,
            'zonestat.SOAOutv4': 0.000000,
            'zonestat.SOAOutv6': 0.000000,
            'zonestat.AXFRReqv4': 0.000000,
            'zonestat.AXFRReqv6': 0.000000,
            'zonestat.IXFRReqv4': 0.000000,
            'zonestat.IXFRReqv6': 0.000000,
            'zonestat.XfrSuccess': 0.000000,
            'zonestat.XfrFail': 0.000000,
            'sockstat.UDP4Open': 0.000000,
            'sockstat.UDP6Open': 0.000000,
            'sockstat.TCP4Open': 0.000000,
            'sockstat.TCP6Open': 0.000000,
            'sockstat.UnixOpen': 0.000000,
            'sockstat.UDP4OpenFail': 0.000000,
            'sockstat.UDP6OpenFail': 0.000000,
            'sockstat.TCP4OpenFail': 0.000000,
            'sockstat.TCP6OpenFail': 0.000000,
            'sockstat.UnixOpenFail': 0.000000,
            'sockstat.UDP4Close': 0.000000,
            'sockstat.UDP6Close': 0.000000,
            'sockstat.TCP4Close': 0.000000,
            'sockstat.TCP6Close': 0.000000,
            'sockstat.UnixClose': 0.000000,
            'sockstat.FDWatchClose': 0.000000,
            'sockstat.UDP4BindFail': 0.000000,
            'sockstat.UDP6BindFail': 0.000000,
            'sockstat.TCP4BindFail': 0.000000,
            'sockstat.TCP6BindFail': 0.000000,
            'sockstat.UnixBindFail': 0.000000,
            'sockstat.FdwatchBindFail': 0.000000,
            'sockstat.UDP4ConnFail': 0.000000,
            'sockstat.UDP6ConnFail': 0.000000,
            'sockstat.TCP4ConnFail': 0.000000,
            'sockstat.TCP6ConnFail': 0.000000,
            'sockstat.UnixConnFail': 0.000000,
            'sockstat.FDwatchConnFail': 0.000000,
            'sockstat.UDP4Conn': 0.000000,
            'sockstat.UDP6Conn': 0.000000,
            'sockstat.TCP4Conn': 0.000000,
            'sockstat.TCP6Conn': 0.000000,
            'sockstat.UnixConn': 0.000000,
            'sockstat.FDwatchConn': 0.000000,
            'sockstat.TCP4AcceptFail': 0.000000,
            'sockstat.TCP6AcceptFail': 0.000000,
            'sockstat.UnixAcceptFail': 0.000000,
            'sockstat.TCP4Accept': 0.000000,
            'sockstat.TCP6Accept': 0.000000,
            'sockstat.UnixAccept': 0.000000,
            'sockstat.UDP4SendErr': 0.000000,
            'sockstat.UDP6SendErr': 0.000000,
            'sockstat.TCP4SendErr': 0.000000,
            'sockstat.TCP6SendErr': 0.000000,
            'sockstat.UnixSendErr': 0.000000,
            'sockstat.FDwatchSendErr': 0.000000,
            'sockstat.UDP4RecvErr': 0.000000,
            'sockstat.UDP6RecvErr': 0.000000,
            'sockstat.TCP4RecvErr': 0.000000,
            'sockstat.TCP6RecvErr': 0.000000,
            'sockstat.UnixRecvErr': 0.000000,
            'sockstat.FDwatchRecvErr': 0.000000,
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)


################################################################################
if __name__ == "__main__":
    unittest.main()
