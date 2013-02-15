#!/usr/bin/python
# coding=utf-8
################################################################################

import os
from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from test import run_only
from mock import patch

from diamond.collector import Collector
from processresources import ProcessResourcesCollector

################################################################################


def run_only_if_psutil_is_available(func):
    try:
        import psutil
        psutil  # workaround for pyflakes issue #13
    except ImportError:
        psutil = None
    pred = lambda: psutil is not None
    return run_only(func, pred)


class TestProcessResourcesCollector(CollectorTestCase):
    TEST_CONFIG = {
        'interval': 10,
        'process': {
            'postgres': {
                'exe': '^\/usr\/lib\/postgresql\/+d.+d\/bin\/postgres',
                'name': ['postgres', 'pg'],
            },
            'foo': {
                'exe': '^foobar',
            },
            'bar': {
                'name': '^bar',
            },
            'barexe': {
                'exe': 'bar$'
            },
            'diamond-selfmon': {
                'selfmon': 'true',
            }
        }
    }
    SELFMON_PID = 10001  # used for selfmonitoring

    def setUp(self):
        config = get_collector_config('ProcessResourcesCollector',
                                      self.TEST_CONFIG)

        self.collector = ProcessResourcesCollector(config, None)

    def test_import(self):
        self.assertTrue(ProcessResourcesCollector)

    @run_only_if_psutil_is_available
    @patch.object(os, 'getpid')
    @patch.object(Collector, 'publish')
    def test(self, publish_mock, getpid_mock):
        process_info_list = [
            # postgres processes
            {'exe': '/usr/lib/postgresql/9.1/bin/postgres',
             'name': 'postgres',
             'pid': 1427,
             'rss': 9875456,
             'vms': 106852352},
            {'exe': '',
             'name': 'postgres: writer process   ',
             'pid': 1445,
             'rss': 1753088,
             'vms': 106835968},
            {'exe': '',
             'name': 'postgres: wal writer process   ',
             'pid': 1446,
             'rss': 1503232,
             'vms': 106835968},
            {'exe': '',
             'name': 'postgres: autovacuum launcher process   ',
             'pid': 1447,
             'rss': 3989504,
             'vms': 109023232},
            {'exe': '',
             'name': 'postgres: stats collector process   ',
             'pid': 1448,
             'rss': 2400256,
             'vms': 75829248},
            # postgres-y process
            {'exe': '',
             'name': 'posgre: not really',
             'pid': 9999,
             'rss': 999999999999,
             'vms': 999999999999,
            },
            # bar process
            {'exe': '/usr/bin/foo',
             'name': 'bar',
             'pid': 9998,
             'rss': 1,
             'vms': 1
            },
            {'exe': '',
             'name': 'barein',
             'pid': 9997,
             'rss': 1,
             'vms': 1
            },
            {'exe': '/usr/bin/bar',
             'name': '',
             'pid': 9996,
             'rss': 10,
             'vms': 10,
            },
            # diamond self mon process
            {'exe': 'DUMMY',
             'name': 'DUMMY',
             'pid': self.SELFMON_PID,
             'rss': 1234,
             'vms': 90210,
            },
        ]

        class ProcessMock:
            def __init__(self, pid, name, rss, vms, exe=None):
                self.pid = pid
                self.name = name
                self.rss = rss
                self.vms = vms
                if exe is not None:
                    self.exe = exe

            def get_memory_info(self):
                class MemInfo:
                    def __init__(self, rss, vms):
                        self.rss = rss
                        self.vms = vms
                return MemInfo(self.rss, self.vms)

            def get_cpu_percent(self, interval=0.1):
                return 7

        process_iter_mock = (ProcessMock(
            pid=x['pid'],
            name=x['name'],
            rss=x['rss'],
            vms=x['vms'],
            exe=x['exe'])
            for x in process_info_list)

        getpid_mock.return_value = self.SELFMON_PID

        patch_psutil_process_iter = patch('psutil.process_iter',
                                          return_value=process_iter_mock)
        patch_psutil_process_iter.start()
        self.collector.collect()
        patch_psutil_process_iter.stop()

        self.assertPublished(publish_mock, 'postgres.rss',
                             9875456 + 1753088 + 1503232 + 3989504 + 2400256)
        self.assertPublished(publish_mock, 'postgres.vms',
                             106852352 + 106835968 + 106835968 + 109023232 +
                             75829248)
        self.assertPublished(publish_mock, 'foo.rss', 0)
        self.assertPublished(publish_mock, 'bar.rss', 2)
        self.assertPublished(publish_mock, 'barexe.rss', 10)
        self.assertPublished(publish_mock, 'diamond-selfmon.rss', 1234)
        self.assertPublished(publish_mock, 'diamond-selfmon.vms', 90210)
        self.assertPublished(publish_mock, 'bar.cpu_percent', 7 * 2)
        self.assertPublished(publish_mock, 'barexe.cpu_percent', 7)

################################################################################
if __name__ == "__main__":
    unittest.main()
