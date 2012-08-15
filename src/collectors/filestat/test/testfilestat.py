#!/usr/bin/python
# coding=utf-8
################################################################################

from test import *

from diamond.collector import Collector
from filestat import FilestatCollector

################################################################################

class TestFilestatCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('FilestatCollector', {
            'interval': 10
        })

        self.collector = FilestatCollector(config, None)

    @patch('__builtin__.open')
    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_open_proc_sys_fs_file_nr(self, publish_mock, open_mock):
        open_mock.return_value = StringIO('')
        self.collector.collect()
        open_mock.assert_called_once_with('/proc/sys/fs/file-nr')

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        FilestatCollector.PROC = self.getFixturePath('proc_sys_fs_file-nr')
        self.collector.collect()

        metrics = {
            'assigned' : 576,
            'unused'   : 0,
            'max'      : 4835852
        }

        self.setDocExample(self.collector.__class__.__name__, metrics)
        self.assertPublishedMany(publish_mock, metrics)

################################################################################
if __name__ == "__main__":
    unittest.main()
