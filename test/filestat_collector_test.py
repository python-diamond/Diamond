#!/usr/bin/python
################################################################################

from common import *

from diamond.collector import Collector
from filestat_collector import FilestatCollector

################################################################################

class TestFilestatCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('FilestatCollector', {
            'interval': 10
        })

        self.collector = FilestatCollector(config, None)

    @patch('__builtin__.open')
    @patch.object(Collector, 'publish')
    def test_should_open_proc_sys_fs_file_nr(self, publish_mock, open_mock):
        open_mock.return_value = StringIO('')
        self.collector.collect()
        open_mock.assert_called_once_with('/proc/sys/fs/file-nr')

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        FilestatCollector.PROC = get_fixture_path('proc_sys_fs_file-nr')
        self.collector.collect()

        self.assertPublishedMany(publish_mock, {
            'assigned' : 576,
            'unused'   : 0,
            'max'      : 4835852
        })

################################################################################
if __name__ == "__main__":
    unittest.main()
