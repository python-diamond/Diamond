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

    def test_import(self):
        self.assertTrue(self.collector.config['path'], 'mesos')

    @patch.object(Collector, 'publish')
    def test_should_work_for_master_with_real_data(self, publish_mock):
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

    @patch.object(Collector, 'publish')
    def test_should_work_for_slave_with_real_data(self, publish_mock):
        config = get_collector_config('MesosCollector', {'master': False})
        self.collector = MesosCollector(config, None)
        self.assertEqual(self.collector.master, False)

        returns = [
            self.getFixture('master_metrics_snapshot.json'),
            self.getFixture('slave_metrics_state.json'),
            self.getFixture('slave_monitor_statistics.json')
        ]

        urlopen_mock = patch('urllib2.urlopen', Mock(
            side_effect=lambda *args: returns.pop(0)))

        urlopen_mock.start()
        self.collector.collect()
        urlopen_mock.stop()

        # check how many fixtures were consumed
        self.assertEqual(urlopen_mock.new.call_count, 3)

        metrics = {
            'master/elected': 1,
            'system/mem_free_bytes': 5663678464.1,
            'registrar/state_store_ms/p9999': (17.8412544, 6),
            'staged_tasks': 20,
            'failed_tasks': 6,
            'finished_tasks': 1,
            'frameworks.marathon-0_7_6.executors.task_name.cpus_limit': (1.7, 1),
            'frameworks.marathon-0_7_6.executors.task_name.instances_count': (2, 0),
            'frameworks.marathon-0_7_6.executors.com_domain_group_anotherApp.mem_mapped_file_bytes': 45056,
            'frameworks.marathon-0_7_6.executors.task_name.mem_percent': (0.19, 2)
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

    @patch.object(Collector, 'publish')
    def test_should_compute_cpus_utilisation(self, publish_mock):
        self.fixture_cpu_utilisation(publish_mock)

        self.assertPublished(
            publish_mock,
            'frameworks.marathon-0_7_6.executors.task_name.cpus_utilisation',
            0.5)

    @patch.object(Collector, 'publish')
    def test_should_compute_cpus_percent(self, publish_mock):
        self.fixture_cpu_utilisation(publish_mock)

        self.assertPublished(
            publish_mock,
            'frameworks.marathon-0_7_6.executors.task_name.cpus_percent',
            0.5/1.7)

    def fixture_cpu_utilisation(self, publish_mock):
        config = get_collector_config('MesosCollector', {'master': False})
        self.collector = MesosCollector(config, None)
        self.assertEqual(self.collector.master, False)
        # we need 2 collect calls to see new metrics
        returns = [
            self.getFixture('master_metrics_snapshot.json'),
            self.getFixture('slave_metrics_state.json'),
            self.getFixture(
                'slave_monitor_statistics_cpus_utilisation_next.json'),
            self.getFixture('master_metrics_snapshot.json'),
            self.getFixture('slave_metrics_state.json'),
            self.getFixture('slave_monitor_statistics_cpus_utilisation.json'),
        ]
        urlopen_mock = patch('urllib2.urlopen', Mock(
            side_effect=lambda *args: returns.pop(0)))
        urlopen_mock.start()
        self.collector.collect()
        publish_mock.reset_mock()
        self.collector.collect()
        urlopen_mock.stop()


if __name__ == "__main__":
    unittest.main()
