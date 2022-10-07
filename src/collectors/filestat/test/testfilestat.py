#!/usr/bin/python
# coding=utf-8
##########################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import patch
from mock import mock_open


from diamond.collector import Collector
from filestat import FilestatCollector

##########################################################################


class TestFilestatCollector(CollectorTestCase):

    def setUp(self):
        config = get_collector_config('FilestatCollector', {
            'interval': 10
        })

        self.collector = FilestatCollector(config, None)

    def test_import(self):
        self.assertTrue(FilestatCollector)

    def mock_lsof_output(self):

        def get_output(fmt):
            fixture = self.getFixturePath('lsof_%s' % (fmt))
            with open(fixture) as output:
                return output.readlines()

        return get_output

    @patch.object(Collector, 'publish')
    def test_shoud_list_users(self, publish_mock):
        with patch.object(FilestatCollector, 'get_output', side_effect=self.mock_lsof_output()) as mock_output:
            self.assertEqual(self.collector.get_userlist(), ['root'])
            mock_output.assert_called_once_with('L')

    @patch.object(Collector, 'publish')
    def test_shoud_list_types(self, publish_mock):
        with patch.object(FilestatCollector, 'get_output', side_effect=self.mock_lsof_output()) as mock_output:
            self.assertEqual(self.collector.get_typelist(), ['CHR', 'FIFO', 'REG', 'DIR'])
            mock_output.assert_called_once_with('t')

    @patch.object(Collector, 'publish')
    def test_should_open_proc_sys_fs_file_nr(self, publish_mock):
        with patch('__builtin__.open', mock_open(read_data='')) as open_mock:
            self.collector.collect()
            open_mock.assert_called_once_with('/proc/sys/fs/file-nr')

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        with patch.object(FilestatCollector, 'PROC', self.getFixturePath('proc_sys_fs_file-nr'), spec=FilestatCollector.PROC):
            self.collector.collect()

        metrics = {
            'assigned': 576,
            'unused': 0,
            'max': 4835852
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

    @patch.object(Collector, 'publish')
    def test_shoud_collect_user_data(self, publish_mock):
        self.collector.config['collect_user_data'] = True
        with patch.object(FilestatCollector, 'PROC', self.getFixturePath('proc_sys_fs_file-nr'), spec=FilestatCollector.PROC):
            with patch.object(FilestatCollector, 'get_output', side_effect=self.mock_lsof_output()) as mock_output:
                self.collector.collect()

        mock_output.assert_any_call('tL')
        mock_output.assert_any_call('t')
        mock_output.assert_any_call('L')

        metrics = {
            'user.root.CHR': 7,
            'user.root.FIFO': 4,
            'user.root.REG': 15,
            'user.root.DIR': 8,
        }

        self.assertPublishedMany(publish_mock, metrics)

##########################################################################
if __name__ == "__main__":
    unittest.main()
