#!/usr/bin/python
# coding=utf-8
################################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import Mock
from mock import patch

from diamond.collector import Collector
from postqueue import PostqueueCollector

################################################################################


class TestPostqueueCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('PostqueueCollector', {
        })

        self.collector = PostqueueCollector(config, {})

    def test_import(self):
        self.assertTrue(PostqueueCollector)

    @patch.object(Collector, 'publish')
    def test_should_work_with_emails_in_queue(self, publish_mock):
        patch_collector = patch.object(PostqueueCollector,
                                       'get_postqueue_output',
                                       Mock(return_value=self.getFixture(
                                        'postqueue_emails').getvalue()))
        patch_collector.start()
        self.collector.collect()
        patch_collector.stop()

        metrics = {
            'count': 3
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])

        self.assertPublishedMany(publish_mock, metrics)

    @patch.object(Collector, 'publish')
    def test_should_work_with_empty_queue(self, publish_mock):
        patch_collector = patch.object(PostqueueCollector,
                                       'get_postqueue_output',
                                       Mock(return_value=self.getFixture(
                                        'postqueue_empty').getvalue()))
        patch_collector.start()
        self.collector.collect()
        patch_collector.stop()

        metrics = {
            'count': 0
        }

        self.assertPublishedMany(publish_mock, metrics)

################################################################################
if __name__ == "__main__":
    unittest.main()
