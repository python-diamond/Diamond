#!/usr/bin/python
# coding=utf-8
##########################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest

from mock import patch, Mock

from diamond.collector import Collector
from openstackswiftrecon import OpenstackSwiftReconCollector


class TestOpenstackSwiftReconCollector(CollectorTestCase):
    def setUp(self, allowed_names=None):
        if not allowed_names:
            allowed_names = []
        config = get_collector_config('OpenstackSwiftReconCollector', {
            'allowed_names': allowed_names,
            'interval': 1,
            'recon_object_cache': self.getFixturePath('object.recon'),
            'recon_container_cache': self.getFixturePath('container.recon'),
            'recon_account_cache': self.getFixturePath('account.recon')
        })
        self.collector = OpenstackSwiftReconCollector(config, None)

    def test_import(self):
        self.assertTrue(OpenstackSwiftReconCollector)

    @patch('__builtin__.open')
    @patch('os.access', Mock(return_value=False))
    @patch.object(Collector, 'publish')
    def test_recon_no_access(self, publish_mock, open_mock):
        self.assertFalse(open_mock.called)
        self.assertFalse(publish_mock.called)

    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_recon_publish(self, publish_mock):
        self.collector.collect()
        metrics = {'object.object_replication_time': 2409.806068432331,
                   'object.object_auditor_stats_ALL.passes': 43887,
                   'object.object_auditor_stats_ALL.errors': 0,
                   'object.object_auditor_stats_ALL.audit_time':
                   301695.1047577858,
                   'object.object_auditor_stats_ALL.start_time':
                   1357979417.104742,
                   'object.object_auditor_stats_ALL.quarantined': 0,
                   'object.object_auditor_stats_ALL.bytes_processed':
                   24799969235,
                   'object.async_pending': 0,
                   'object.object_updater_sweep': 0.767723798751831,
                   'object.object_auditor_stats_ZBF.passes': 99350,
                   'object.object_auditor_stats_ZBF.errors': 0,
                   'object.object_auditor_stats_ZBF.audit_time':
                   152991.46442770958,
                   'object.object_auditor_stats_ZBF.start_time':
                   1357979462.621007,
                   'object.object_auditor_stats_ZBF.quarantined': 0,
                   'object.object_auditor_stats_ZBF.bytes_processed': 0}
        self.assertPublishedMany(publish_mock, metrics)

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])

##########################################################################
if __name__ == "__main__":
    unittest.main()
