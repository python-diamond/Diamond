#!/usr/bin/python
# coding=utf-8
##########################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import patch, Mock

from diamond.collector import Collector
from nvidia_gpu import NvidiaGPUCollector

##########################################################################


class TestNvidiaGPUCollector(CollectorTestCase):

    def setUp(self):
        config = get_collector_config('NvidiaGPUCollector', {
        })

        self.collector = NvidiaGPUCollector(config, None)

    def test_import(self):
        self.assertTrue(NvidiaGPUCollector)

    @patch.object(Collector, 'publish')
    def test_should_publish_gpu_stat(self, publish_mock):
        output_mock = Mock(
            return_value=(self.getFixture('nvidia_smi').getvalue(), '')
        )
        collector_mock = patch.object(
            NvidiaGPUCollector,
            'run_command',
            output_mock
        )

        collector_mock.start()
        self.collector.collect()
        collector_mock.stop()

        metrics = {
            'gpu_0.memory.total': 4095,
            'gpu_0.memory.used': 2670,
            'gpu_0.memory.free': 1425,
            'gpu_0.utilization.gpu': 0,
            'gpu_0.utilization.memory': 0,
            'gpu_0.temperature.gpu': 53,
            'gpu_1.memory.total': 4095,
            'gpu_1.memory.used': 2670,
            'gpu_1.memory.free': 1425,
            'gpu_1.utilization.gpu': 0,
            'gpu_1.utilization.memory': 0,
            'gpu_1.temperature.gpu': 44,
            'gpu_2.memory.total': 4095,
            'gpu_2.memory.used': 1437,
            'gpu_2.memory.free': 2658,
            'gpu_2.utilization.gpu': 0,
            'gpu_2.utilization.memory': 0,
            'gpu_2.temperature.gpu': 48,
            'gpu_3.memory.total': 4095,
            'gpu_3.memory.used': 1437,
            'gpu_3.memory.free': 2658,
            'gpu_3.utilization.gpu': 0,
            'gpu_3.utilization.memory': 0,
            'gpu_3.temperature.gpu': 44
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)


##########################################################################
if __name__ == "__main__":
    unittest.main()
