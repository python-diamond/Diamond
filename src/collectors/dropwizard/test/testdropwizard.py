#!/usr/bin/python
# coding=utf-8
################################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import Mock
from mock import patch

from diamond.collector import Collector

from dropwizard import DropwizardCollector

################################################################################


class TestDropwizardCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('DropwizardCollector', {})

        self.collector = DropwizardCollector(config, None)

    def test_import(self):
        self.assertTrue(DropwizardCollector)

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        patch_urlopen = patch('urllib2.urlopen',
                              Mock(return_value=self.getFixture('stats')))

        patch_urlopen.start()
        self.collector.collect()
        patch_urlopen.stop()

        metrics = {
            'jvm.memory.totalInit': 9.142272E7,
            'jvm.memory.totalUsed': 1.29674584E8,
            'jvm.memory.totalMax': 1.13901568E9,
            'jvm.memory.totalCommitted': 1.62267136E8,
            'jvm.memory.heapInit': 6.7108864E7,
            'jvm.memory.heapUsed': 8.3715232E7,
            'jvm.memory.heapMax': 9.54466304E8,
            'jvm.memory.heapCommitted': 1.15539968E8,
            'jvm.memory.heap_usage': 0.08770894441130528,
            'jvm.memory.non_heap_usage': 0.24903553182428534,
            'jvm.memory.code_cache': 0.038289388020833336,
            'jvm.memory.eden_space': 0.1918924383560846,
            'jvm.memory.old_gen': 0.022127459689416828,
            'jvm.memory.perm_gen': 0.32806533575057983,
            'jvm.memory.survivor_space': 1.0,
            'jvm.daemon_thread_count': 10,
            'jvm.thread_count': 27,
            'jvm.fd_usage': 0.014892578125,
            'jvm.thread_states.timed_waiting': 0.5185185185185185,
            'jvm.thread_states.runnable': 0.0,
            'jvm.thread_states.blocked': 0.0,
            'jvm.thread_states.waiting': 0.2222222222222222,
            'jvm.thread_states.new': 0.0,
            'jvm.thread_states.terminated': 0.0
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

    @patch.object(Collector, 'publish')
    def test_should_fail_gracefully(self, publish_mock):
        patch_urlopen = patch('urllib2.urlopen',
                              Mock(
                                return_value=self.getFixture('stats_blank')))

        patch_urlopen.start()
        self.collector.collect()
        patch_urlopen.stop()

        self.assertPublishedMany(publish_mock, {})

################################################################################
if __name__ == "__main__":
    unittest.main()
