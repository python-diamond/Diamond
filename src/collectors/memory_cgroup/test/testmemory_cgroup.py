#!/usr/bin/python
# coding=utf-8
################################################################################
import os
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
from memory_cgroup import MemoryCgroupCollector

dirname = os.path.dirname(__file__)
fixtures_path = os.path.join(dirname, 'fixtures/')
fixtures = []
for root, dirnames, filenames in os.walk(fixtures_path):
    fixtures.append([root, dirnames, filenames])


class TestMemoryCgroupCollector(CollectorTestCase):

    def test_import(self):
        self.assertTrue(MemoryCgroupCollector)

    @patch('__builtin__.open')
    @patch('os.walk', Mock(return_value=iter(fixtures)))
    @patch.object(Collector, 'publish')
    def test_should_open_all_memory_stat(self, publish_mock, open_mock):
        config = get_collector_config('MemoryCgroupCollector', {
            'interval': 10,
            'byte_unit': 'megabyte'
        })

        self.collector = MemoryCgroupCollector(config, None)
        open_mock.side_effect = lambda x: StringIO('')
        self.collector.collect()
        open_mock.assert_any_call(
            fixtures_path + 'lxc/testcontainer/memory.stat')
        open_mock.assert_any_call(fixtures_path + 'lxc/memory.stat')
        open_mock.assert_any_call(fixtures_path + 'memory.stat')

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        config = get_collector_config('MemoryCgroupCollector', {
            'interval': 10,
            'byte_unit': 'megabyte',
            'memory_path': fixtures_path
        })

        self.collector = MemoryCgroupCollector(config, None)
        self.collector.collect()

        self.assertPublishedMany(publish_mock, {
            'lxc.testcontainer.cache': 1,
            'lxc.testcontainer.rss': 1,
            'lxc.testcontainer.swap': 1,
            'lxc.cache': 1,
            'lxc.rss': 1,
            'lxc.swap': 1,
            'system.cache': 1,
            'system.rss': 1,
            'system.swap': 1,
            'lxc.testcontainer.total_cache': 1,
            'lxc.testcontainer.total_rss': 1,
            'lxc.testcontainer.total_swap': 1,
            'lxc.total_cache': 1,
            'lxc.total_rss': 1,
            'lxc.total_swap': 1,
            'system.total_cache': 1,
            'system.total_rss': 1,
            'system.total_swap': 1,
        })

    @patch.object(Collector, 'publish')
    def test_should_not_include_filtered_metrics(self, publish_mock):
        config = get_collector_config('MemoryCgroupCollector', {
            'interval': 10,
            'byte_unit': 'megabyte',
            'memory_path': fixtures_path,
            'skip': 'test\w+ner',
        })

        self.collector = MemoryCgroupCollector(config, None)
        self.collector.collect()

        should_be_published = {
            'lxc.cache': 1,
            'lxc.rss': 1,
            'lxc.swap': 1,
            'system.cache': 1,
            'system.rss': 1,
            'system.swap': 1,
            'lxc.total_cache': 1,
            'lxc.total_rss': 1,
            'lxc.total_swap': 1,
            'system.total_cache': 1,
            'system.total_rss': 1,
            'system.total_swap': 1,
        }
        should_not_be_published = {
            'lxc.testcontainer.cache': 1,
            'lxc.testcontainer.rss': 1,
            'lxc.testcontainer.swap': 1,
            'lxc.testcontainer.total_cache': 1,
            'lxc.testcontainer.total_rss': 1,
            'lxc.testcontainer.total_swap': 1,
        }
        [self.assertPublished(publish_mock, k, v)
         for k, v in should_be_published.iteritems()]
        [self.assertUnpublished(publish_mock, k, v)
         for k, v in should_not_be_published.iteritems()]

if __name__ == "__main__":
    unittest.main()
