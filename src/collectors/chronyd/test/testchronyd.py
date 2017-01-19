#!/usr/bin/python
# coding=utf-8
##########################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import Mock
from mock import patch

from diamond.collector import Collector
from chronyd import ChronydCollector

##########################################################################


class TestChronydCollector(CollectorTestCase):

    def setUp(self):
        config = get_collector_config('ChronydCollector', {
        })

        self.collector = ChronydCollector(config, {})

    def test_import(self):
        self.assertTrue(ChronydCollector)

    @patch.object(Collector, 'publish')
    def test_should_work_with_ip_addresses(self, publish_mock):
        patch_collector = patch.object(
            ChronydCollector,
            'get_output',
            Mock(return_value=self.getFixture(
                'fedora').getvalue()))
        patch_collector.start()
        self.collector.collect()
        patch_collector.stop()

        metrics = {
            '178_251_120_16.offset_ms': -7e-05,
            '85_12_29_43.offset_ms': -0.785,
            '85_234_197_3.offset_ms': 0.08,
            '85_255_214_66.offset_ms': 0.386,
        }

        self.setDocExample(
            collector=self.collector.__class__.__name__,
            metrics=metrics,
            defaultpath=self.collector.config['path'])

        self.assertPublishedMany(publish_mock, metrics)

    @patch.object(Collector, 'publish')
    def test_should_work_with_fqdns(self, publish_mock):
        patch_collector = patch.object(
            ChronydCollector,
            'get_output',
            Mock(return_value=self.getFixture(
                'fqdn').getvalue()))
        patch_collector.start()
        self.collector.collect()
        patch_collector.stop()

        metrics = {
            'adm-dns-resolver-001.offset_ms': 0.000277,
            'adm-dns-resolver-002.offset_ms': 0.456,
        }

        self.assertPublishedMany(publish_mock, metrics)

    @patch.object(Collector, 'publish')
    def test_check_invalid_unit(self, publish_mock):
        patch_collector = patch.object(
            ChronydCollector,
            'get_output',
            Mock(return_value=self.getFixture(
                'bad_unit').getvalue()))
        patch_collector.start()
        self.collector.collect()
        patch_collector.stop()

        metrics = {
            'adm-dns-resolver-002.offset_ms': 0.456,
        }

        self.assertPublishedMany(publish_mock, metrics)

    @patch.object(Collector, 'publish')
    def test_huge_values(self, publish_mock):
        patch_collector = patch.object(
            ChronydCollector,
            'get_output',
            Mock(return_value=self.getFixture(
                'huge_vals').getvalue()))
        patch_collector.start()
        self.collector.collect()
        patch_collector.stop()

        metrics = {
            'server1.offset_ms': 8735472000000,
            'server2.offset_ms': -1009152000000,
        }

        self.assertPublishedMany(publish_mock, metrics)

##########################################################################
if __name__ == "__main__":
    unittest.main()
