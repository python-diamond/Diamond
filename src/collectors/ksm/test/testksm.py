#!/usr/bin/python
################################################################################

from test import *

from diamond.collector import Collector
from ksm import KSMCollector

################################################################################

class TestKSMCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('KSMCollector', {
            'interval': 10,
            'ksm_path': os.path.dirname(__file__)+'/fixtures/'
        })

        self.collector = KSMCollector(config, None)

    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_work_with_synthetic_data(self, publish_mock):
        self.collector.collect()

        self.assertPublishedMany(publish_mock, {
            'full_scans' : 123.0, 
            'pages_shared' : 124.0, 
            'pages_sharing' : 125.0, 
            'pages_to_scan' : 100.0, 
            'pages_unshared' : 126.0, 
            'pages_volatile' : 127.0, 
            'run' : 1.0, 
            'sleep_millisecs' : 20.0, 
        })

################################################################################
if __name__ == "__main__":
    unittest.main()
