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
from diskspace import DiskSpaceCollector

################################################################################


def run_only_if_major_is_available(func):
    try:
        import os
        os.major
        major = True
    except AttributeError:
        major = None
    pred = lambda: major is not None
    return run_only(func, pred)


class TestDiskSpaceCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('DiskSpaceCollector', {
            'interval': 10,
            'byte_unit': ['gigabyte'],
            'exclude_filters': [
                '^/export/home',
                '^/tmpfs',
            ]
        })

        self.collector = DiskSpaceCollector(config, None)

    def test_import(self):
        self.assertTrue(DiskSpaceCollector)

    @run_only_if_major_is_available
    @patch('os.access', Mock(return_value=True))
    def test_get_file_systems(self):
        result = None

        os_stat_mock = patch('os.stat')
        os_major_mock = patch('os.major')
        os_minor_mock = patch('os.minor')
        open_mock = patch('__builtin__.open',
                          Mock(return_value=self.getFixture('proc_mounts')))

        stat_mock = os_stat_mock.start()
        stat_mock.return_value.st_dev = 42

        major_mock = os_major_mock.start()
        major_mock.return_value = 9

        minor_mock = os_minor_mock.start()
        minor_mock.return_value = 0

        omock = open_mock.start()

        result = self.collector.get_file_systems()
        os_stat_mock.stop()
        os_major_mock.stop()
        os_minor_mock.stop()
        open_mock.stop()

        stat_mock.assert_called_once_with('/')
        major_mock.assert_called_once_with(42)
        minor_mock.assert_called_once_with(42)

        self.assertEqual(result, {
            (9, 0): {
                'device':
                '/dev/disk/by-uuid/81969733-a724-4651-9cf5-64970f86daba',
                'fs_type': 'ext3',
                'mount_point': '/'}
        })

        omock.assert_called_once_with('/proc/mounts')
        return result

    @run_only_if_major_is_available
    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        statvfs_mock = Mock()
        statvfs_mock.f_bsize = 4096
        statvfs_mock.f_frsize = 4096
        statvfs_mock.f_blocks = 360540255
        statvfs_mock.f_bfree = 285953527
        statvfs_mock.f_bavail = 267639130
        statvfs_mock.f_files = 91578368
        statvfs_mock.f_ffree = 91229495
        statvfs_mock.f_favail = 91229495
        statvfs_mock.f_flag = 4096
        statvfs_mock.f_namemax = 255

        os_stat_mock = patch('os.stat')
        os_major_mock = patch('os.major', Mock(return_value=9))
        os_minor_mock = patch('os.minor', Mock(return_value=0))
        os_path_isdir_mock = patch('os.path.isdir', Mock(return_value=False))
        open_mock = patch('__builtin__.open',
                          Mock(return_value=self.getFixture('proc_mounts')))
        os_statvfs_mock = patch('os.statvfs', Mock(return_value=statvfs_mock))

        os_stat_mock.start()
        os_major_mock.start()
        os_minor_mock.start()
        os_path_isdir_mock.start()
        open_mock.start()
        os_statvfs_mock.start()
        self.collector.collect()
        os_stat_mock.stop()
        os_major_mock.stop()
        os_minor_mock.stop()
        os_path_isdir_mock.stop()
        open_mock.stop()
        os_statvfs_mock.stop()

        metrics = {
            'root.gigabyte_used': (284.525, 2),
            'root.gigabyte_free': (1090.826, 2),
            'root.gigabyte_avail': (1020.962, 2),
            'root.inodes_used': 348873,
            'root.inodes_free': 91229495,
            'root.inodes_avail': 91229495
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

################################################################################
if __name__ == "__main__":
    unittest.main()
