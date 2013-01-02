#!/usr/bin/python
# coding=utf-8
################################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from test import run_only
from mock import Mock
from mock import patch

from diamond.collector import Collector
from beanstalkd import BeanstalkdCollector

################################################################################


def run_only_if_beanstalkc_is_available(func):
    try:
        import beanstalkc
        beanstalkc  # workaround for pyflakes issue #13
    except ImportError:
        beanstalkc = None
    pred = lambda: beanstalkc is not None
    return run_only(func, pred)


class TestBeanstalkdCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('BeanstalkdCollector', {
            'host': 'localhost',
            'port': 11300,
        })

        self.collector = BeanstalkdCollector(config, None)

    def test_import(self):
        self.assertTrue(BeanstalkdCollector)

    @run_only_if_beanstalkc_is_available
    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        stats = {
            'instance': {
                'current-connections': 10,
                'max-job-size': 65535,
                'cmd-release': 0,
                'cmd-reserve': 4386,
                'pid': 23703,
                'cmd-bury': 0,
                'current-producers': 0,
                'total-jobs': 4331,
                'current-jobs-ready': 0,
                'cmd-peek-buried': 0,
                'current-tubes': 7,
                'current-jobs-delayed': 0,
                'uptime': 182954,
                'cmd-watch': 55,
                'job-timeouts': 0,
                'cmd-stats': 1,
                'rusage-stime': 295.970497,
                'current-jobs-reserved': 0,
                'current-jobs-buried': 0,
                'cmd-reserve-with-timeout': 0,
                'cmd-put': 4331,
                'cmd-pause-tube': 0,
                'cmd-list-tubes-watched': 0,
                'cmd-list-tubes': 0,
                'current-workers': 9,
                'cmd-list-tube-used': 0,
                'cmd-ignore': 0,
                'binlog-records-migrated': 0,
                'current-waiting': 9,
                'cmd-peek': 0,
                'cmd-peek-ready': 0,
                'cmd-peek-delayed': 0,
                'cmd-touch': 0,
                'binlog-oldest-index': 0,
                'binlog-current-index': 0,
                'cmd-use': 4321,
                'total-connections': 4387,
                'cmd-delete': 4331,
                'binlog-max-size': 10485760,
                'cmd-stats-job': 0,
                'rusage-utime': 125.92787,
                'cmd-stats-tube': 0,
                'binlog-records-written': 0,
                'cmd-kick': 0,
                'current-jobs-urgent': 0,
            },
            'tubes': [
                {
                    'current-jobs-delayed': 0,
                    'pause': 0,
                    'name': 'default',
                    'cmd-pause-tube': 0,
                    'current-jobs-buried': 0,
                    'cmd-delete': 10,
                    'pause-time-left': 0,
                    'current-waiting': 9,
                    'current-jobs-ready': 0,
                    'total-jobs': 10,
                    'current-watching': 10,
                    'current-jobs-reserved': 0,
                    'current-using': 10,
                    'current-jobs-urgent': 0,
                }
             ]
        }

        patch_get_stats = patch.object(BeanstalkdCollector,
                                        '_get_stats',
                                        Mock(return_value=stats))

        patch_get_stats.start()
        self.collector.collect()
        patch_get_stats.stop()

        metrics = {
            'current-connections': 10,
            'max-job-size': 65535,
            'cmd-release': 0,
            'cmd-reserve': 4386,
            'pid': 23703,
            'cmd-bury': 0,
            'current-producers': 0,
            'total-jobs': 4331,
            'current-jobs-ready': 0,
            'cmd-peek-buried': 0,
            'current-tubes': 7,
            'current-jobs-delayed': 0,
            'uptime': 182954,
            'cmd-watch': 55,
            'job-timeouts': 0,
            'cmd-stats': 1,
            'rusage-stime': 295.970497,
            'current-jobs-reserved': 0,
            'current-jobs-buried': 0,
            'cmd-reserve-with-timeout': 0,
            'cmd-put': 4331,
            'cmd-pause-tube': 0,
            'cmd-list-tubes-watched': 0,
            'cmd-list-tubes': 0,
            'current-workers': 9,
            'cmd-list-tube-used': 0,
            'cmd-ignore': 0,
            'binlog-records-migrated': 0,
            'current-waiting': 9,
            'cmd-peek': 0,
            'cmd-peek-ready': 0,
            'cmd-peek-delayed': 0,
            'cmd-touch': 0,
            'binlog-oldest-index': 0,
            'binlog-current-index': 0,
            'cmd-use': 4321,
            'total-connections': 4387,
            'cmd-delete': 4331,
            'binlog-max-size': 10485760,
            'cmd-stats-job': 0,
            'rusage-utime': 125.92787,
            'cmd-stats-tube': 0,
            'binlog-records-written': 0,
            'cmd-kick': 0,
            'current-jobs-urgent': 0,
            'tubes.default.current-jobs-delayed': 0,
            'tubes.default.pause': 0,
            'tubes.default.cmd-pause-tube': 0,
            'tubes.default.current-jobs-buried': 0,
            'tubes.default.cmd-delete': 10,
            'tubes.default.pause-time-left': 0,
            'tubes.default.current-waiting': 9,
            'tubes.default.current-jobs-ready': 0,
            'tubes.default.total-jobs': 10,
            'tubes.default.current-watching': 10,
            'tubes.default.current-jobs-reserved': 0,
            'tubes.default.current-using': 10,
            'tubes.default.current-jobs-urgent': 0,
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

################################################################################
if __name__ == "__main__":
    unittest.main()
