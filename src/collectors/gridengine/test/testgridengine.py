#!/usr/bin/python
# coding=utf-8

from test import CollectorTestCase
from test import get_collector_config
from mock import patch
import os

from diamond.collector import Collector
from gridengine import GridEngineCollector


class TestGridEngineCollector(CollectorTestCase):
    """Set up the fixtures for the test
    """
    def setUp(self):
        config = get_collector_config('GridEngineCollector', {})
        self.collector = GridEngineCollector(config, None)
        self.fixtures_dir = os.path.abspath(os.path.join(
                os.path.dirname(__file__), 'fixtures'))

    def test_import(self):
        """Test that import succeeds
        """
        self.assertTrue(GridEngineCollector)

    @patch.object(GridEngineCollector, '_queue_stats_xml')
    @patch.object(Collector, 'publish')
    def test_queue_stats_should_work_with_real_data(self, publish_mock,
            xml_mock):
        """Test that fixtures are parsed correctly
        """
        xml_mock.return_value = self.getFixture('queue_stats.xml').getvalue()
        self.collector._collect_queue_stats()

        published_metrics = {
            'queues.hadoop.load': 0.00532,
            'queues.hadoop.used': 0,
            'queues.hadoop.resv': 0,
            'queues.hadoop.available': 0,
            'queues.hadoop.total': 36,
            'queues.hadoop.temp_disabled': 0,
            'queues.hadoop.manual_intervention': 36,
            'queues.primary_q.load': 0.20509,
            'queues.primary_q.used': 1024,
            'queues.primary_q.resv': 0,
            'queues.primary_q.available': 1152,
            'queues.primary_q.total': 2176,
            'queues.primary_q.temp_disabled': 0,
            'queues.primary_q.manual_intervention': 0,
            'queues.secondary_q.load': 0.00460,
            'queues.secondary_q.used': 145,
            'queues.secondary_q.resv': 0,
            'queues.secondary_q.available': 1007,
            'queues.secondary_q.total': 1121,
            'queues.secondary_q.temp_disabled': 1,
            'queues.secondary_q.manual_intervention': 0
        }
        self.assertPublishedMany(publish_mock, published_metrics)
