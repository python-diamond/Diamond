#!/usr/bin/python
################################################################################

from common import *

from diamond.collector import Collector
import disk

################################################################################

class TestDisk(unittest.TestCase):
    @patch('__builtin__.open')
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

            result = disk.get_file_systems()

            os_stat_mock.assert_called_once_with('/')
            os_major_mock.assert_called_once_with(42)
            os_minor_mock.assert_called_once_with(42)

            self.assertEqual(result, {
                (9, 0) : ('/dev/disk/by-uuid/81969733-a724-4651-9cf5-64970f86daba', '/')
            })

        open_mock.assert_called_once_with('/proc/mounts')
        return result

    @patch('__builtin__.open')
    def test_get_disk_statistics(self, open_mock):
        result = None
        open_mock.return_value = StringIO("""
   1       0 ram0 0 0 0 0 0 0 0 0 0 0 0
   1       1 ram1 0 0 0 0 0 0 0 0 0 0 0
   1       2 ram2 0 0 0 0 0 0 0 0 0 0 0
   1       3 ram3 0 0 0 0 0 0 0 0 0 0 0
   1       4 ram4 0 0 0 0 0 0 0 0 0 0 0
   1       5 ram5 0 0 0 0 0 0 0 0 0 0 0
   1       6 ram6 0 0 0 0 0 0 0 0 0 0 0
   1       7 ram7 0 0 0 0 0 0 0 0 0 0 0
   1       8 ram8 0 0 0 0 0 0 0 0 0 0 0
   1       9 ram9 0 0 0 0 0 0 0 0 0 0 0
   1      10 ram10 0 0 0 0 0 0 0 0 0 0 0
   1      11 ram11 0 0 0 0 0 0 0 0 0 0 0
   1      12 ram12 0 0 0 0 0 0 0 0 0 0 0
   1      13 ram13 0 0 0 0 0 0 0 0 0 0 0
   1      14 ram14 0 0 0 0 0 0 0 0 0 0 0
   1      15 ram15 0 0 0 0 0 0 0 0 0 0 0
   7       0 loop0 0 0 0 0 0 0 0 0 0 0 0
   7       1 loop1 0 0 0 0 0 0 0 0 0 0 0
   7       2 loop2 0 0 0 0 0 0 0 0 0 0 0
   7       3 loop3 0 0 0 0 0 0 0 0 0 0 0
   7       4 loop4 0 0 0 0 0 0 0 0 0 0 0
   7       5 loop5 0 0 0 0 0 0 0 0 0 0 0
   7       6 loop6 0 0 0 0 0 0 0 0 0 0 0
   7       7 loop7 0 0 0 0 0 0 0 0 0 0 0
   8       0 sda 11296323 127761523 1114247280 165221020 9292767 32155242 333252048 208563560 0 19035310 374755270
   8       1 sda1 11296296 127761523 1114247064 165220780 9292767 32155242 333252048 208563560 0 19035230 374755030
   8      16 sdb 11334585 127760303 1114502518 162448600 9287483 32167260 333227008 189022120 0 18792930 352418270
   8      17 sdb1 11334558 127760303 1114502302 162448420 9287483 32167260 333227008 189022120 0 18792870 352418090
   8      32 sdc 11357096 128084136 1117263302 175647900 9071409 31921768 329475344 181140140 0 19509790 357693530
   8      33 sdc1 11357069 128084136 1117263086 175647670 9071409 31921768 329475344 181140140 0 19509740 357693300
   8      48 sdd 11350168 128344871 1119269534 168467240 9130464 31774918 328709208 167823720 0 18473250 337157280
   8      49 sdd1 11350141 128344871 1119269318 168467050 9130464 31774918 328709208 167823720 0 18473200 337157090
   9       0 md0 150707 0 2818762 0 111152210 0 889217680 0 0 0 0
        """.strip())

        result = disk.get_disk_statistics()

        open_mock.assert_called_once_with('/proc/diskstats')
        
        self.assertItemsEqual(
            result.keys(),
            [ (8,  0), (8,  1), (8, 16), (8, 17), (8, 32), (8, 33), (8, 48), (8, 49), (9,  0) ]
        )

        return result

################################################################################
if __name__ == "__main__":
    unittest.main()
