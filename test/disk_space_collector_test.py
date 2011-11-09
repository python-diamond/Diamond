#!/usr/bin/python
################################################################################

from common import *

from diamond.collector import Collector
from disk_space_collector import DiskSpaceCollector

import disk

################################################################################

class TestDiskSpaceCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('DiskSpaceCollector', {
            'interval': 10
        })

        self.collector = DiskSpaceCollector(config, None)

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
            patch('os.major', return_value = 9),
            patch('os.minor', return_value = 0),
            patch('__builtin__.open', return_value = get_fixture('proc_mounts'))
        ):
            file_systems = disk.get_file_systems()

        with nested(
            patch('disk.get_file_systems', return_value = file_systems),
            patch('os.statvfs', return_value = statvfs_mock)
        ):
            self.collector.collect()

        self.assertPublishedMany(publish_mock, {
            'root.gbytes_used'  : ( 284.525, 2),
            'root.gbytes_free'  : (1090.826, 2),
            'root.gbytes_avail' : (1020.962, 2),
            'root.inodes_used'  : 348873,
            'root.inodes_free'  : 91229495,
            'root.inodes_avail' : 91229495
        })

        publish_mock.reset_mock()        

################################################################################
if __name__ == "__main__":
    unittest.main()
