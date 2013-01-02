#!/usr/bin/python
# coding=utf-8
################################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import Mock
from mock import patch

from diamond.collector import Collector
from apcupsd import ApcupsdCollector

################################################################################


class TestApcupsdCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('ApcupsdCollector', {
            'interval': 10
        })

        self.collector = ApcupsdCollector(config, None)

    def test_import(self):
        self.assertTrue(ApcupsdCollector)

    @patch.object(Collector, 'publish')
    def test_should_work_with_synthetic_data(self, publish_mock):
        patch_getdata = patch.object(ApcupsdCollector, 'getData', Mock(
            return_value='APC      : 001,039,1056\n\x00\'DATE     : 2012-07-16 '
            + '12:53:58 -0700  \n\x00 HOSTNAME : localhost\n\x00+VERSION  : 3.1'
            + '4.8 (16 January 2010) redhat\n\x00 UPSNAME  : localhost\n\x00'
            + '\x15CABLE    : USB Cable\n\x00\x1dMODEL    : Back-UPS BX1300G '
            + '\n\x00\x17UPSMODE  : Stand Alone\n\x00\'STARTTIME: 2011-12-07 '
            + '10:28:24 -0800  \n\x00\x13STATUS   : ONLINE \n\x00\x17LINEV    '
            + ': 124.0 Volts\n\x00\'LOADPCT  :   5.0 Percent Load Capacity\n'
            + '\x00\x19BCHARGE  : 100.0 Percent\n\x00\x19TIMELEFT :  73.9'
            + ' Minutes\n\x00\x15MBATTCHG : 5 Percent\n\x00\x15MINTIMEL : 3'
            + ' Minutes\n\x00\x15MAXTIME  : 0 Seconds\n\x00\x12SENSE    :'
            + ' Medium\n\x00\x17LOTRANS  : 088.0 Volts\n\x00\x17HITRANS  :'
            + ' 139.0 Volts\n\x00\x12ALARMDEL : Always\n\x00\x16BATTV    :'
            + ' 27.3 Volts\n\x00+LASTXFER : Automatic or explicit self test'
            + '\n\x00\x0eNUMXFERS : 19\n\x00\'XONBATT  : 2012-07-13 09:11:52'
            + ' -0700  \n\x00\x15TONBATT  : 0 seconds\n\x00\x17CUMONBATT: 130'
            + ' seconds\n\x00\'XOFFBATT : 2012-07-13 09:12:01 -0700  \n\x00\''
            + 'LASTSTEST: 2012-07-13 09:11:52 -0700  \n\x00\x0eSELFTEST : NO\n'
            + '\x00"STATFLAG : 0x07000008 Status Flag\n\x00\x16MANDATE  : 2009'
            + '-10-08\n\x00\x1aSERIALNO : 3B0941X40219  \n\x00\x16BATTDATE :'
            + ' 2009-10-08\n\x00\x15NOMINV   : 120 Volts\n\x00\x17NOMBATTV :'
                + '  24.0 '))

        patch_getdata.start()
        self.collector.collect()
        patch_getdata.stop()

        metrics = {
            'localhost.LINEV': 124.000000,
            'localhost.LOADPCT': 5.000000,
            'localhost.BCHARGE': 100.000000,
            'localhost.TIMELEFT': 73.900000,
            'localhost.BATTV': 27.300000,
            'localhost.NUMXFERS': 0.000000,
            'localhost.TONBATT': 0.000000,
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])

        self.assertPublishedMany(publish_mock, metrics)

################################################################################
if __name__ == "__main__":
    unittest.main()
