#!/usr/bin/python
################################################################################

from test import *

from diamond.collector import Collector
from diskspace import DiskSpaceCollector

################################################################################

class TestDiskSpaceCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('DiskSpaceCollector', {
            'interval'  : 10,
            'byte_unit' : 'gigabyte'
        })

        self.collector = DiskSpaceCollector(config, None)
        
    @patch('__builtin__.open')
    @patch('os.access', Mock(return_value=True))

    def test_get_file_systems(self, open_mock):
        result = None
        open_mock.return_value = StringIO("""
rootfs / rootfs rw 0 0
none /sys sysfs rw,nosuid,nodev,noexec,relatime 0 0
none /proc proc rw,nosuid,nodev,noexec,relatime 0 0
none /dev devtmpfs rw,relatime,size=24769364k,nr_inodes=6192341,mode=755 0 0
none /dev/pts devpts rw,nosuid,noexec,relatime,gid=5,mode=620,ptmxmode=000 0 0
fusectl /sys/fs/fuse/connections fusectl rw,relatime 0 0
/dev/disk/by-uuid/81969733-a724-4651-9cf5-64970f86daba / ext3 rw,relatime,errors=continue,barrier=0,data=ordered 0 0
none /sys/kernel/debug debugfs rw,relatime 0 0
none /sys/kernel/security securityfs rw,relatime 0 0
none /dev/shm tmpfs rw,nosuid,nodev,relatime 0 0
none /var/run tmpfs rw,nosuid,relatime,mode=755 0 0
none /var/lock tmpfs rw,nosuid,nodev,noexec,relatime 0 0
        """.strip())

        with nested(
            patch('os.stat'), patch('os.major'), patch('os.minor')
        ) as (os_stat_mock, os_major_mock, os_minor_mock):
            os_stat_mock.return_value.st_dev = 42
            os_major_mock.return_value = 9
            os_minor_mock.return_value = 0

            result = self.collector.get_file_systems()

            os_stat_mock.assert_called_once_with('/')
            os_major_mock.assert_called_once_with(42)
            os_minor_mock.assert_called_once_with(42)

            self.assertEqual(result, {
                (9, 0) : {'device' : '/dev/disk/by-uuid/81969733-a724-4651-9cf5-64970f86daba', 'mount_point' : '/'}
            })

        open_mock.assert_called_once_with('/proc/mounts')
        return result

    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        statvfs_mock = Mock()
        statvfs_mock.f_bsize   = 4096
        statvfs_mock.f_frsize  = 4096
        statvfs_mock.f_blocks  = 360540255
        statvfs_mock.f_bfree   = 285953527
        statvfs_mock.f_bavail  = 267639130
        statvfs_mock.f_files   = 91578368
        statvfs_mock.f_ffree   = 91229495
        statvfs_mock.f_favail  = 91229495
        statvfs_mock.f_flag    = 4096
        statvfs_mock.f_namemax = 255

        with nested(
            patch('os.stat'),
            patch('os.major', Mock(return_value = 9)),
            patch('os.minor', Mock(return_value = 0)),
            patch('os.path.isdir', Mock(return_value = False)),
            patch('__builtin__.open', Mock(return_value = self.getFixture('proc_mounts'))),
            patch('os.statvfs', Mock(return_value = statvfs_mock))
        ):
            self.collector.collect()

        self.assertPublishedMany(publish_mock, {
            'root.gigabyte_used'  : ( 284.525, 2),
            'root.gigabyte_free'  : (1090.826, 2),
            'root.gigabyte_avail' : (1020.962, 2),
            'root.inodes_used'    : 348873,
            'root.inodes_free'    : 91229495,
            'root.inodes_avail'   : 91229495
        })

################################################################################
if __name__ == "__main__":
    unittest.main()
