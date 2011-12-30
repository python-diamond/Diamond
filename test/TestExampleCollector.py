#!/usr/bin/python
################################################################################

from common import *

from diamond.collector import Collector
from ExampleCollector import ExampleCollector

################################################################################

class TestExampleCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('MemoryCollector', {
            'interval'  : 10
        })

        self.collector = ExampleCollector(config, None)

    @patch.object(Collector, 'publish')
    def test(self, publish_mock):
        self.collector.collect()

        self.assertPublishedMany(publish_mock, {
            'my.example.metric' :  42
        })

################################################################################
if __name__ == "__main__":
    unittest.main()
