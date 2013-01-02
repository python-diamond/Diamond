#!/usr/bin/python
# coding=utf-8
################################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import Mock
from mock import patch

from diamond.collector import Collector
from nagios import NagiosStatsCollector

################################################################################


class TestNagiosStatsCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('NagiosStatsCollector', {
            'interval': 10,
            'bin': 'true',
            'use_sudo': False
        })

        self.collector = NagiosStatsCollector(config, None)

    def test_import(self):
        self.assertTrue(NagiosStatsCollector)

    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        patch_communicate = patch('subprocess.Popen.communicate',
                                  Mock(return_value=(
                                    self.getFixture('nagiostat').getvalue(),
                                    '')))

        patch_communicate.start()
        self.collector.collect()
        patch_communicate.stop()

        metrics = {
            'AVGACTHSTLAT': 196,
            'AVGACTSVCLAT': 242,
            'AVGACTHSTEXT': 4037,
            'AVGACTSVCEXT': 340,
            'NUMHSTUP': 63,
            'NUMHSTDOWN': 0,
            'NUMHSTUNR': 0,
            'NUMSVCOK': 1409,
            'NUMSVCWARN': 3,
            'NUMSVCUNKN': 0,
            'NUMSVCCRIT': 7,
            'NUMHSTACTCHK5M': 56,
            'NUMHSTPSVCHK5M': 0,
            'NUMSVCACTCHK5M': 541,
            'NUMSVCPSVCHK5M': 0,
            'NUMACTHSTCHECKS5M': 56,
            'NUMOACTHSTCHECKS5M': 1,
            'NUMCACHEDHSTCHECKS5M': 1,
            'NUMSACTHSTCHECKS5M': 55,
            'NUMPARHSTCHECKS5M': 55,
            'NUMSERHSTCHECKS5M': 0,
            'NUMPSVHSTCHECKS5M': 0,
            'NUMACTSVCCHECKS5M': 1101,
            'NUMOACTSVCCHECKS5M': 0,
            'NUMCACHEDSVCCHECKS5M': 0,
            'NUMSACTSVCCHECKS5M': 1101,
            'NUMPSVSVCCHECKS5M': 0,
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

################################################################################
if __name__ == "__main__":
    unittest.main()
