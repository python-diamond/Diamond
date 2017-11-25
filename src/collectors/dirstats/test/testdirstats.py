#!/usr/bin/python
# coding=utf-8
##########################################################################

from stat import S_IFDIR, S_IFREG

from test import CollectorTestCase
from test import get_collector_config
from test import unittest

from time import time

from mock import Mock
from mock import patch

from diamond.collector import Collector
from dirstats import DirStatsCollector, DAY, MB

##########################################################################


class EntityMock(object):

    def __init__(self, is_file):

        if is_file:

            self.st_mode = S_IFREG
            self.st_size = MB
            self.st_mtime = time()-(DAY*7)
            self.st_blocks = 1024

        else:

            self.st_mode = S_IFDIR
            self.st_mtime = time()-(DAY*5)


class TestDirStatsCollector(CollectorTestCase):

    def setUp(self):
        config = get_collector_config('DirStatsCollector', {
            'interval': 10,
            'dirs': {
                'logs': '/var/log/'}
            })

        self.collector = DirStatsCollector(config, None)

    def entity_side_effect(self, path):

        if 'file' in path:
            return EntityMock(is_file=True)

        return EntityMock(is_file=False)

    def test_import(self):
        self.assertTrue(DirStatsCollector)

    @patch.object(Collector, 'publish')
    def test_non_empty_directory(self, publish_mock):
        patch_listdir = patch('os.listdir', Mock(
            side_effect=[

                # root level
                #
                # /var/log/DIR_1
                # /var/log/DIR_2
                # /var/log/DIR_3
                # /var/log/file_1
                # /var/log/file_2

                ['DIR_1', 'DIR_2', 'DIR_3', 'file_1', 'file_2'],

                # dir1 level
                #
                # /var/log/DIR_1/DIR_4
                # /var/log/DIR_1/file_3
                # /var/log/DIR_1/file_4
                # /var/log/DIR_1/file_5
                # /var/log/DIR_1/file_6

                ['DIR_4', 'file_3', 'file_4', 'file_5', 'file_6'],

                # dir2 level
                #
                # /var/log/DIR_2/file_7
                # /var/log/DIR_2/file_8
                # /var/log/DIR_2/DIR_5
                # /var/log/DIR_2/file_9
                # /var/log/DIR_2/file_10

                ['file_7', 'file_8', 'DIR_5', 'file_9', 'file_10'],

                # dir3 is empty, dir1/dir4 level
                #
                # /var/log/DIR_1/DIR_4/file_11
                # /var/log/DIR_1/DIR_4/file_12
                # /var/log/DIR_1/DIR_4/file_13
                # /var/log/DIR_1/DIR_4/file_14

                [], ['file_11', 'file_12', 'file_13', 'file_14'],

                # dir2/dir5 level
                #
                # /var/log/DIR_2/DIR_5/file_15
                # /var/log/DIR_2/DIR_5/file_16
                # /var/log/DIR_2/DIR_5/file_17
                # /var/log/DIR_2/DIR_5/file_18

                ['file_15', 'file_16', 'file_17', 'file_18']]

            ))

        patch_stat = patch('os.stat', Mock(
            side_effect=self.entity_side_effect
            ))

        patch_listdir.start()
        patch_stat.start()
        self.collector.collect()
        patch_listdir.stop()
        patch_stat.stop()

        self.assertPublishedMany(publish_mock, {
            'logs.size.current': 9,
            'logs.size.allocated': 18,
            'logs.subdirs': 5,
            'logs.files': 18,
            'logs.days_unmodified': 7
        })

    @patch.object(Collector, 'publish')
    def test_empty_directory(self, publish_mock):
        patch_listdir = patch('os.listdir', Mock(return_value=[]))

        patch_stat = patch('os.stat', Mock(
            side_effect=self.entity_side_effect
            ))

        patch_listdir.start()
        patch_stat.start()
        self.collector.collect()
        patch_listdir.stop()
        patch_stat.stop()

        self.assertPublishedMany(publish_mock, {
            'logs.size.current': 0,
            'logs.size.allocated': 0,
            'logs.subdirs': 0,
            'logs.files': 0,
            'logs.days_unmodified': 5
        })


##########################################################################
if __name__ == "__main__":
    unittest.main()
