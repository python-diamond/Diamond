#!/usr/bin/python
# coding=utf-8
################################################################################
import os
from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import Mock
from mock import patch

try:
    from cStringIO import StringIO
    StringIO  # workaround for pyflakes issue #13
except ImportError:
    from StringIO import StringIO

from diamond.collector import Collector
from cpuacct_cgroup import CpuAcctCgroupCollector

dirname = os.path.dirname(__file__)
fixtures_path = os.path.join(dirname, 'fixtures/')
fixtures = []
for root, dirnames, filenames in os.walk(fixtures_path):
    fixtures.append([root, dirnames, filenames])


class TestCpuAcctCgroupCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('CpuAcctCgroupCollector', {
            'interval': 10
        })

        self.collector = CpuAcctCgroupCollector(config, None)

    def test_import(self):
        self.assertTrue(CpuAcctCgroupCollector)

    @patch('__builtin__.open')
    @patch('os.walk', Mock(return_value=iter(fixtures)))
    @patch.object(Collector, 'publish')
    def test_should_open_all_cpuacct_stat(self, publish_mock, open_mock):
        open_mock.side_effect = lambda x: StringIO('')
        self.collector.collect()
        open_mock.assert_any_call(
            fixtures_path + 'lxc/testcontainer/cpuacct.stat')
        open_mock.assert_any_call(fixtures_path + 'lxc/cpuacct.stat')
        open_mock.assert_any_call(fixtures_path + 'cpuacct.stat')

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        CpuAcctCgroupCollector.CPUACCT_PATH = fixtures_path
        self.collector.collect()

        self.assertPublishedMany(publish_mock, {
            'lxc.testcontainer.user': 1318,
            'lxc.testcontainer.system': 332,
            'lxc.user': 36891,
            'lxc.system': 88927,
            'system.user': 3781253,
            'system.system': 4784004,
        })

if __name__ == "__main__":
    unittest.main()
