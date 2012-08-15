#!/usr/bin/python
# coding=utf-8
################################################################################

from test import *

from diamond.collector import Collector
from ipvs import IPVSCollector

################################################################################

class TestIPVSCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('IPVSCollector', {
            'interval': 10,
            'bin' : 'true',
            'use_sudo' : False
        })

        self.collector = IPVSCollector(config, None)

    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        with patch('subprocess.Popen.communicate', Mock(return_value =
            ( self.getFixture('ipvsadm').getvalue() , '')
        )):
            self.collector.collect()

        metrics = {
            "172_16_1_56:80.total.conns" : 116,
            "172_16_1_56:443.total.conns" : 59,
            "172_16_1_56:443.10_68_15_66:443.conns" : 59,
            "172_16_1_56:443.10_68_15_66:443.outbytes" : 216873,
        }
        
        self.setDocExample(self.collector.__class__.__name__, metrics)
        self.assertPublishedMany(publish_mock, metrics)

################################################################################
if __name__ == "__main__":
    unittest.main()
