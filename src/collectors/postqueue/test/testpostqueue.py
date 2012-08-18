#!/usr/bin/python
# coding=utf-8
################################################################################

from test import CollectorTestCase
from test import get_collector_config
from mock import Mock
from mock import patch

from diamond.collector import Collector
from postqueue import PostqueueCollector

################################################################################


class TestPostqueueCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('PostqueueCollector', {})

        self.collector = PostqueueCollector(config, {})

    @patch.object(Collector, 'publish_metric')
    def test_should_work_with_emails_in_queue(self, publish_mock):
        with patch.object(PostqueueCollector,
                          'get_postqueue_output',
                          Mock(return_value=self.getFixture(
                            'postqueue_emails').getvalue())):
            self.collector.collect()

        self.assertPublishedMetric(publish_mock, 'count', 3)

    @patch.object(Collector, 'publish_metric')
    def test_should_work_with_empty_queue(self, publish_mock):
        with patch.object(PostqueueCollector,
                          'get_postqueue_output',
                          Mock(return_value=self.getFixture(
                            'postqueue_empty').getvalue())):
            self.collector.collect()

        self.assertPublishedMetric(publish_mock, 'count', 0)

################################################################################
if __name__ == "__main__":
    unittest.main()
