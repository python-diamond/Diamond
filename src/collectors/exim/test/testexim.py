#!/usr/bin/python
################################################################################

from test import *

from diamond.collector import Collector
from exim import EximCollector

################################################################################

class TestEximCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('EximCollector', {
            'interval': 10
        })

        self.collector = EximCollector(config, None)
        self.collector.COMMAND[0] = 'true'

    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_work_with_synthetic_data(self, publish_mock):
        with patch('subprocess.Popen.communicate', Mock(return_value =
            ( '33' , '')
        )):
            self.collector.collect()
            
        self.assertPublishedMany(publish_mock, {
            'queuesize' : 33.0
        })

    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_fail_gracefully(self, publish_mock):
        with patch('subprocess.Popen.communicate', Mock(return_value =
            ( '' , '')
        )):
            self.collector.collect()

        self.assertPublishedMany(publish_mock, {})

    @patch('os.access', Mock(return_value=False))
    @patch.object(Collector, 'publish')
    def test_should_fail_gracefully_2(self, publish_mock):
        self.collector.collect()
        self.assertPublishedMany(publish_mock, {})

################################################################################
if __name__ == "__main__":
    unittest.main()
