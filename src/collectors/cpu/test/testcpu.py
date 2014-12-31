#!/usr/bin/python
# coding=utf-8
################################################################################

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
from cpu import CPUCollector

################################################################################


class TestCPUCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('CPUCollector', {
            'interval': 10,
            'normalize': False
        })

        self.collector = CPUCollector(config, None)

    def test_import(self):
        self.assertTrue(CPUCollector)

    @patch('__builtin__.open')
    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_open_proc_stat(self, publish_mock, open_mock):
        CPUCollector.PROC = '/proc/stat'
        open_mock.return_value = StringIO('')
        self.collector.collect()
        open_mock.assert_called_once_with('/proc/stat')

    @patch.object(Collector, 'publish')
    def test_should_work_with_synthetic_data(self, publish_mock):
        patch_open = patch('__builtin__.open', Mock(return_value=StringIO(
            'cpu 100 200 300 400 500 0 0 0 0 0')))

        patch_open.start()
        self.collector.collect()
        patch_open.stop()

        self.assertPublishedMany(publish_mock, {})

        patch_open = patch('__builtin__.open', Mock(return_value=StringIO(
            'cpu 110 220 330 440 550 0 0 0 0 0')))

        patch_open.start()
        self.collector.collect()
        patch_open.stop()

        self.assertPublishedMany(publish_mock, {
            'total.idle': 4.0,
            'total.iowait': 5.0,
            'total.nice': 2.0,
            'total.system': 3.0,
            'total.user': 1.0
        })

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        CPUCollector.PROC = self.getFixturePath('proc_stat_1')
        self.collector.collect()

        self.assertPublishedMany(publish_mock, {})

        CPUCollector.PROC = self.getFixturePath('proc_stat_2')
        self.collector.collect()

        metrics = {
            'total.idle': 2440.8,
            'total.iowait': 0.2,
            'total.nice': 0.0,
            'total.system': 0.2,
            'total.user': 0.4
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

    @patch.object(Collector, 'publish')
    def test_should_work_with_ec2_data(self, publish_mock):
        self.collector.config['interval'] = 30
        patch_open = patch('os.path.isdir', Mock(return_value=True))
        patch_open.start()

        CPUCollector.PROC = self.getFixturePath('ec2_stat_1')
        self.collector.collect()

        self.assertPublishedMany(publish_mock, {})

        CPUCollector.PROC = self.getFixturePath('ec2_stat_2')
        self.collector.collect()

        patch_open.stop()

        metrics = {
            'total.idle': 68.4,
            'total.iowait': 0.6,
            'total.nice': 0.0,
            'total.system': 13.7,
            'total.user': 16.666666666666668
        }

        self.assertPublishedMany(publish_mock, metrics)

    @patch.object(Collector, 'publish')
    def test_473(self, publish_mock):
        """
        No cpu value should ever be over 100
        """
        self.collector.config['interval'] = 60
        patch_open = patch('os.path.isdir', Mock(return_value=True))
        patch_open.start()

        CPUCollector.PROC = self.getFixturePath('473_1')
        self.collector.collect()

        self.assertPublishedMany(publish_mock, {})

        CPUCollector.PROC = self.getFixturePath('473_2')
        self.collector.collect()

        patch_open.stop()

        totals = {}

        for call in publish_mock.mock_calls:
            call = call[1]
            if call[0][:6] == 'total.':
                continue
            if call[1] > 100:
                raise ValueError("metric %s: %s should not be over 100!" % (
                    call[0], call[1]))
            k = call[0][:4]
            totals[k] = totals.get(k, 0) + call[1]

        for t in totals:
            # Allow rounding errors
            if totals[t] >= 101:
                raise ValueError(
                    "metric total for %s: %s should not be over 100!" % (
                        t, totals[t]))


class TestCPUCollectorNormalize(CollectorTestCase):

    def setUp(self):
        config = get_collector_config('CPUCollector', {
            'interval': 1,
            'normalize': True,
        })

        self.collector = CPUCollector(config, None)

        self.num_cpu = 2

        # first measurement
        self.input_base = {
            'user': 100,
            'nice': 200,
            'system': 300,
            'idle': 400,
        }
        # second measurement
        self.input_next = {
            'user': 110,
            'nice': 220,
            'system': 330,
            'idle': 440,
        }
        # expected increment, divided by number of CPUs
        # for example, user should be 10/2 = 5
        self.expected = {
            'total.user': 5.0,
            'total.nice': 10.0,
            'total.system': 15.0,
            'total.idle': 20.0,
        }

    # convert an input dict with values to a string that might come from
    # /proc/stat
    def input_dict_to_proc_string(self, cpu_id, dict_):
        return ("cpu%s %i %i %i %i 0 0 0 0 0 0" %
                (cpu_id,
                 dict_['user'],
                 dict_['nice'],
                 dict_['system'],
                 dict_['idle'],
                 )
                )

    @patch.object(Collector, 'publish')
    def test_should_work_proc_stat(self, publish_mock):
        patch_open = patch('__builtin__.open', Mock(return_value=StringIO(
            "\n".join([self.input_dict_to_proc_string('', self.input_base),
                       self.input_dict_to_proc_string('0', self.input_base),
                       self.input_dict_to_proc_string('1', self.input_base),
                       ])
        )))

        patch_open.start()
        self.collector.collect()
        patch_open.stop()

        self.assertPublishedMany(publish_mock, {})

        patch_open = patch('__builtin__.open', Mock(return_value=StringIO(
            "\n".join([self.input_dict_to_proc_string('', self.input_next),
                       self.input_dict_to_proc_string('0', self.input_next),
                       self.input_dict_to_proc_string('1', self.input_next),
                       ])
        )))

        patch_open.start()
        self.collector.collect()
        patch_open.stop()

        self.assertPublishedMany(publish_mock, self.expected)

    @patch.object(Collector, 'publish')
    @patch('cpu.os')
    @patch('cpu.psutil')
    def test_should_work_psutil(self, psutil_mock, os_mock, publish_mock):

        os_mock.access.return_value = False

        total = Mock(**self.input_base)
        cpu_time = [Mock(**self.input_base),
                    Mock(**self.input_base),
                    ]
        psutil_mock.cpu_times.side_effect = [cpu_time, total]

        self.collector.collect()

        self.assertPublishedMany(publish_mock, {})

        total = Mock(**self.input_next)
        cpu_time = [Mock(**self.input_next),
                    Mock(**self.input_next),
                    ]
        psutil_mock.cpu_times.side_effect = [cpu_time, total]

        self.collector.collect()

        self.assertPublishedMany(publish_mock, self.expected)

################################################################################
if __name__ == "__main__":
    unittest.main()
