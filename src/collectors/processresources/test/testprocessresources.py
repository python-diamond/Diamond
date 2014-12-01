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
                'exe': '^\/usr\/bin\/foo',
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
            {
                'exe': '/usr/lib/postgresql/9.1/bin/postgres',
                'name': 'postgres',
                'pid': 1427,
                'rss': 1000000,
                'vms': 1000000
            },
            {
                'exe': '',
                'name': 'postgres: writer process   ',
                'pid': 1445,
                'rss': 100000,
                'vms': 200000
            },
            {
                'exe': '',
                'name': 'postgres: wal writer process   ',
                'pid': 1446,
                'rss': 10000,
                'vms': 20000
            },
            {
                'exe': '',
                'name': 'postgres: autovacuum launcher process   ',
                'pid': 1447,
                'rss': 1000,
                'vms': 2000
            },
            {
                'exe': '',
                'name': 'postgres: stats collector process   ',
                'pid': 1448,
                'rss': 100,
                'vms': 200},
            # postgres-y process
            {
                'exe': '',
                'name': 'posgre: not really',
                'pid': 9999,
                'rss': 10,
                'vms': 20,
            },
            {
                'exe': '/usr/bin/foo',
                'name': 'bar',
                'pid': 9998,
                'rss': 1,
                'vms': 1
            },
            {
                'exe': '',
                'name': 'barein',
                'pid': 9997,
                'rss': 2,
                'vms': 2
            },
            {
                'exe': '/usr/bin/bar',
                'name': '',
                'pid': 9996,
                'rss': 3,
                'vms': 3,
            },
            # diamond self mon process
            {
                'exe': 'DUMMY',
                'name': 'DUMMY',
                'pid': self.SELFMON_PID,
                'rss': 1234,
                'vms': 4,
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

                self.cmdline = [self.exe]

            def as_dict(self):
                from collections import namedtuple
                meminfo = namedtuple('meminfo', 'rss vms')
                ext_meminfo = namedtuple('meminfo',
                                         'rss vms shared text lib data dirty')
                cputimes = namedtuple('cputimes', 'user system')
                openfile = namedtuple('openfile', 'path fd')
                thread = namedtuple('thread', 'id user_time system_time')
                user = namedtuple('user', 'real effective saved')
                group = namedtuple('group', 'real effective saved')
                io = namedtuple('io',
                                'read_count write_count read_bytes write_bytes')
                ionice = namedtuple('ionice', 'ioclass value')
                amount = namedtuple('amount', 'voluntary involuntary')
                return {
                    'status': 'sleeping',
                    'num_ctx_switches': amount(voluntary=2243, involuntary=221),
                    'pid': self.pid,
                    'connections': None,
                    'cmdline': [self.exe],
                    'create_time': 1389294592.02,
                    'ionice': ionice(ioclass=0, value=0),
                    'num_fds': None,
                    'memory_maps': None,
                    'cpu_percent': 0.0,
                    'terminal': None,
                    'ppid': 0,
                    'cwd': None,
                    'nice': 0,
                    'username': 'root',
                    'cpu_times': cputimes(user=0.27, system=1.05),
                    'io_counters': None,
                    'ext_memory_info': ext_meminfo(rss=self.rss,
                                                   vms=self.vms,
                                                   shared=1310720,
                                                   text=188416,
                                                   lib=0,
                                                   data=868352,
                                                   dirty=0),
                    'threads': [thread(id=1, user_time=0.27, system_time=1.04)],
                    'open_files': None,
                    'name': self.name,
                    'num_threads': 1,
                    'exe': self.exe,
                    'uids': user(real=0, effective=0, saved=0),
                    'gids': group(real=0, effective=0, saved=0),
                    'cpu_affinity': [0, 1, 2, 3],
                    'memory_percent': 0.03254831000922748,
                    'memory_info': meminfo(rss=self.rss, vms=self.vms)}

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
        self.assertPublished(publish_mock, 'postgres.ext_memory_info.rss',
                             1000000 + 100000 + 10000 + 1000 + 100)
        self.assertPublished(publish_mock, 'foo.ext_memory_info.rss', 1)
        self.assertPublished(publish_mock, 'bar.ext_memory_info.rss', 3)
        self.assertPublished(publish_mock, 'barexe.ext_memory_info.rss', 3)
        self.assertPublished(publish_mock,
                             'diamond-selfmon.ext_memory_info.rss', 1234)

################################################################################
if __name__ == "__main__":
    unittest.main()
