#!/usr/bin/python
# coding=utf-8
################################################################################

from test import *

from diamond.collector import Collector
from resqueweb import ResqueWebCollector

################################################################################


class TestResqueWebCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('ResqueWebCollector', {
            'interval': 10
        })

        self.collector = ResqueWebCollector(config, None)

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        with patch('urllib2.urlopen', Mock(
            return_value=self.getFixture('stats.txt'))):
            self.collector.collect()

        metrics = {
            'pending.current': 2,
            'processed.total': 11686516,
            'failed.total': 38667,
            'workers.current': 9,
            'working.current': 2,
            'queue.low.current': 4,
            'queue.mail.current': 3,
            'queue.realtime.current': 9,
            'queue.normal.current': 1,
        }

        self.setDocExample(self.collector.__class__.__name__, metrics)
        self.assertPublishedMany(publish_mock, metrics)

    @patch.object(Collector, 'publish')
    def test_should_fail_gracefully(self, publish_mock):
        with patch('urllib2.urlopen', Mock(
            return_value=self.getFixture('stats_blank.txt'))):
            self.collector.collect()

        self.assertPublishedMany(publish_mock, {})

################################################################################
if __name__ == "__main__":
    unittest.main()
