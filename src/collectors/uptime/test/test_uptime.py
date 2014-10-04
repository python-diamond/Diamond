#!/usr/bin/python
# coding=utf-8
###############################################################################

from test import CollectorTestCase
from test import get_collector_config
from mock import Mock
from mock import patch

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from diamond.collector import Collector
from uptime import UptimeCollector

###############################################################################


class TestUptimeCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('UptimeCollector', {
            'interval': 10,
        })

        self.collector = UptimeCollector(config, None)

    def test_import(self):
        self.assertTrue(UptimeCollector)

    @patch('__builtin__.open')
    @patch('os.path.exists', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_open_proc_uptime(self, publish_mock, open_mock):
        open_mock.return_value = StringIO('1288459.83 10036802.26')
        self.collector.collect()
        open_mock.assert_called_once_with('/proc/uptime')

    @patch.object(Collector, 'publish')
    def test_sanity_check(self, publish_mock):
        self.collector.PROC = self.getFixturePath('sanity_check')
        self.collector.collect()

        self.assertPublishedMany(publish_mock, {
            'minutes': 60
        })

    @patch.object(Collector, 'publish')
    def test_malformed_input(self, publish_mock):
        self.collector.PROC = self.getFixturePath('malformed_input')
        self.collector.collect()
        self.collector.PROC = self.getFixturePath('sanity_check')
        self.collector.collect()

        self.assertPublishedMany(publish_mock, {
            'minutes': 60.0
        })
