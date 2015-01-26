#!/usr/bin/python
# coding=utf-8

from mock import Mock
from mock import patch

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from diamond.collector import Collector
from mesos import MesosCollector


class TestMesosCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('MesosCollector', {})

        self.collector = MesosCollector(config, None)

    def test_import(self):
        self.assertTrue(MesosCollector)

    def test_get_default_config(self):
        self.collector.get_default_config_help() == {
            'host': '127.0.0.1',
            'port': 5050,
            'path': 'metrics/snapshot',
        }

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        returns = self.getFixture('master_metrics_snapshot.json')
        urlopen_mock = patch('urllib2.urlopen', Mock(
            side_effect=lambda *args: returns))

        urlopen_mock.start()
        self.collector.collect()
        urlopen_mock.stop()

        # check how many fixtures were consumed
        self.assertEqual(urlopen_mock.new.call_count, 1)

        metrics = {
            'master/elected': (1, 0),
            "system/mem_free_bytes": (5663678464.1, 0),
            "registrar/state_store_ms/p9999": (17.8412544, 6)
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)


if __name__ == "__main__":
    unittest.main()
