#!/usr/bin/python
# coding=utf-8
##########################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import Mock
from mock import patch

from diamond.collector import Collector

from mesos import MesosCollector

##########################################################################


class TestMesosCollector(CollectorTestCase):

    def setUp(self):
        config = get_collector_config('MesosCollector', {})

        self.collector = MesosCollector(config, None)

    def test_import(self):
        self.assertTrue(MesosCollector)

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        def se(url):
            if url == 'http://localhost:5051/state.json':
                return self.getFixture('state.json')

        patch_urlopen = patch('urllib2.urlopen', Mock(side_effect=se))

        patch_urlopen.start()
        self.collector.collect()
        patch_urlopen.stop()

        metrics = self.valid_metrics()
        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

    def valid_metrics(self):
        return {
            'master.cpus_percent': 0.762166666666667,
            'master.cpus_total': 120,
            'master.cpus_used': 91.46,
            'master.disk_percent': 0.0317975447795468,
            'master.disk_total': 12541440,
            'master.disk_used': 398787
        }

##########################################################################
if __name__ == "__main__":
    unittest.main()
