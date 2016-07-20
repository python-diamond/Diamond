#!/usr/bin/python
# coding=utf-8

from test import CollectorTestCase
from test import get_collector_config
from test import unittest

from mock import Mock
from mock import patch

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from diamond.collector import Collector
from genericfile import GenericFileCollector


class TestGenericFileCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('GenericFileCollector', {
            'interval': 10,
            'file': '/proc/vmstat',
        })
        self.collector = GenericFileCollector(config, None)

    def test_config(self):
        self.assertTrue(self.collector.config['interval'] == 10)

    def test_match_with_valid_separators(self):
        # space
        line = 'nr_dirty      12'
        stat = self.collector.match(line)

        self.assertEqual(stat, {
            'key': 'nr_dirty',
            'value': '12',
        })

        # colon with surrounding space
        line = 'cache_alignment      : 24'
        stat = self.collector.match(line)

        self.assertEqual(stat, {
            'key': 'cache_alignment',
            'value': '24',
        })

        # equals with no space
        line = 'key=23'
        stat = self.collector.match(line)
        self.assertEqual(stat, {
            'key': 'key',
            'value': '23',
        })

    def test_match_with_invalid_separator(self):
        line = 'nr_dirty -  12'

        none = self.collector.match(line)

        self.assertIsNone(none)

    @patch.object(Collector, 'publish')
    def test_should_publish_valid_metrics(self, publish_mock):
        self.collector.config['file'] = self.getFixturePath('proc_vmstat')

        self.collector.collect()

        # Only a subset of metrics are represented here
        published_metrics = {
            'nr_free_pages': 1849035,
            'nr_inactive_anon': 167,
            'nr_active_anon': 31798,
            'nr_inactive_file': 76916,
            'nr_active_file': 60236,
            'nr_unevictable': 0,
            'nr_mlock': 0,
            'nr_anon_pages': 31760,
            'nr_mapped': 4353,
            'nr_file_pages': 137358,
            'nr_dirty': 0,
            'nr_writeback': 0,
            'nr_slab_reclaimable': 14993,
            'nr_slab_unreclaimable': 3663,
            'nr_page_table_pages': 986,
            'nr_kernel_stack': 123,
            'nr_unstable': 0,
            'nr_bounce': 0,
            'nr_vmscan_write': 0,
            'nr_vmscan_immediate_reclaim': 0,
            'nr_writeback_temp': 0,
            'nr_isolated_anon': 0,
            'nr_isolated_file': 0,
            'nr_shmem': 205,
            'nr_dirtied': 180956,
            'nr_written': 152420,
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=published_metrics,
                           defaultpath=self.collector.config['path'])

        self.assertPublishedMany(publish_mock, published_metrics)

if __name__ == "__main__":
    unittest.main()
