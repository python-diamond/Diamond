#!/usr/bin/python
################################################################################

from test import *

from diamond.collector import Collector
from puppetdashboard import PuppetDashboardCollector

################################################################################

class TestPuppetDashboardCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('PuppetDashboardCollector', {
            'interval': 10
        })

        self.collector = PuppetDashboardCollector(config, None)

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        with patch('urllib2.urlopen', Mock(return_value = self.getFixture('index.html'))):
            self.collector.collect()
            
        self.assertPublishedMany(publish_mock, {
            'unresponsive': 3,
            'pending': 0,
            'changed': 10,
            'unchanged': 4,
            'unreported': 0,
        })

    @patch.object(Collector, 'publish')
    def test_should_fail_gracefully(self, publish_mock):
        with patch('urllib2.urlopen', Mock(return_value = self.getFixture('index.blank'))):
            self.collector.collect()
            
        self.assertPublishedMany(publish_mock, {})

################################################################################
if __name__ == "__main__":
    unittest.main()
