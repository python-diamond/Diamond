#!/usr/bin/python
################################################################################

from test import *

from diamond.collector import Collector
from diskusage import DiskUsageCollector

################################################################################

class TestDiskUsageCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('DiskUsageCollector', {
            'interval'  : 10,
            'byte_unit' : 'kilobyte'
        })

        self.collector = DiskUsageCollector(config, None)

    @patch('__builtin__.open')
    @patch('os.access', Mock(return_value=True))

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

        result = self.collector.get_disk_statistics()

        open_mock.assert_called_once_with('/proc/diskstats')

        self.assertEqual(
            sorted(result.keys()),
            [ (8,  0), (8,  1), (8, 16), (8, 17), (8, 32), (8, 33), (8, 48), (8, 49), (9,  0) ]
        )

        return result

    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):

        with nested(
            patch('__builtin__.open', Mock(return_value = self.getFixture('proc_diskstats_1'))),
            patch('time.time', Mock(return_value = 10))
        ):
            self.collector.collect()

        self.assertPublishedMany(publish_mock, {})

        with nested(
            patch('__builtin__.open', Mock(return_value = self.getFixture('proc_diskstats_2'))),
            patch('time.time', Mock(return_value = 20))
        ):
            self.collector.collect()

        self.assertPublishedMany(publish_mock, {
            'sda.average_queue_length':             0.0,
            'sda.average_request_size_kilobyte':    10.7,
            'sda.await':                            0.0,
            'sda.concurrent_io':                    0.0,
            'sda.io':                               0.3,
            'sda.io_in_progress':                   0.0,
            'sda.io_milliseconds':                  0.0,
            'sda.io_milliseconds_weighted':         0.0,
            'sda.iops':                             0.03,
            'sda.read_kilobyte_per_second':         0.0,
            'sda.read_requests_merged_per_second':  0.0,
            'sda.reads':                            0.0,
            'sda.reads_kilobyte':                   0.0,
            'sda.reads_merged':                     0.0,
            'sda.reads_milliseconds':               0.0,
            'sda.reads_per_second':                 0.0,
            'sda.service_time':                     0.0,
            'sda.util_percentage':                  0.0,
            'sda.write_kilobyte_per_second':        0.32,
            'sda.write_requests_merged_per_second': 0.05,
            'sda.writes':                           0.3,
            'sda.writes_kilobyte':                  3.2,
            'sda.writes_merged':                    0.5,
            'sda.writes_milliseconds':              0.0,
            'sda.writes_per_second':                0.03,
            'sdb.average_queue_length':             49570.0,
            'sdb.average_request_size_kilobyte':    6.3,

            'sdb.await':                            0.8,
            'sdb.concurrent_io':                    0.05,
            'sdb.io':                               921.4,
            'sdb.io_in_progress':                   0,
            'sdb.io_milliseconds':                  495.7,
            'sdb.io_milliseconds_weighted':         749.2,
            'sdb.iops':                             92.14,
            'sdb.read_kilobyte_per_second':         186.24,
            'sdb.read_requests_merged_per_second':  0.0,
            'sdb.reads':                            116.4,
            'sdb.reads_kilobyte':                   1862.4,
            'sdb.reads_merged':                     0.0,
            'sdb.reads_milliseconds':               716.3,
            'sdb.reads_per_second':                 11.64,
            'sdb.service_time':                     0.5,
            'sdb.util_percentage':                  49.57,
            'sdb.write_kilobyte_per_second':        391.43,
            'sdb.write_requests_merged_per_second': 20.17,
            'sdb.writes':                           805.0,
            'sdb.writes_kilobyte':                  3914.3,
            'sdb.writes_merged':                    201.7,
            'sdb.writes_milliseconds':              33.7,
            'sdb.writes_per_second':                80.5,
        })

################################################################################
if __name__ == "__main__":
    unittest.main()
