#!/usr/bin/python
# coding=utf-8
################################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import patch
from mock import Mock

from diamond.collector import Collector
from puppetagent import PuppetAgentCollector

################################################################################


class TestPuppetAgentCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('PuppetAgentCollector', {
            'interval': 10
        })

        self.collector = PuppetAgentCollector(config, None)

        self.last_run_fixture = self.getFixture('last_run_summary.yaml')

    def test_import(self):
        self.assertTrue(PuppetAgentCollector)

    @patch.object(Collector, 'publish')
    def test(self, publish_mock):

        open_mock = patch('__builtin__.open',
                          Mock(return_value=self.getFixture(
                            'last_run_summary.yaml')))

        open_mock.start()
        self.collector.collect()
        open_mock.stop()

        metrics = {
            'changes.total': 1,
            'events.failure': 0,
            'events.success': 1,
            'events.total': 1,
            'resources.changed': 1,
            'resources.failed': 0,
            'resources.failed_to_restart': 0,
            'resources.out_of_sync': 1,
            'resources.restarted': 0,
            'resources.scheduled': 0,
            'resources.skipped': 6,
            'resources.total': 439,
            'time.anchor': 0.009641,
            'time.augeas': 1.286514,
            'time.config_retrieval': 8.06442093849182,
            'time.cron': 0.00089,
            'time.exec': 9.780635,
            'time.file': 1.729348,
            'time.filebucket': 0.000633,
            'time.firewall': 0.007807,
            'time.group': 0.013421,
            'time.last_run': 1377125556,
            'time.mailalias': 0.000335,
            'time.mount': 0.002749,
            'time.package': 1.831337,
            'time.resources': 0.000371,
            'time.service': 0.734021,
            'time.ssh_authorized_key': 0.017625,
            'time.total': 23.5117989384918,
            'time.user': 0.02927,
            'version.config': 1377123965,
        }

        unpublished_metrics = {
            'version.puppet': '2.7.14',
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])

        self.assertPublishedMany(publish_mock, metrics)
        #self.assertUnpublishedMany(publish_mock, unpublished_metrics)

################################################################################
if __name__ == "__main__":
    unittest.main()
