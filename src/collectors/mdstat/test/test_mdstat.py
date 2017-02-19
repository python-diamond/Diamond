#!/usr/bin/env python2
# coding=utf-8

import os
import io
from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import Mock
from mock import patch

from diamond.collector import Collector
from mdstat import MdStatCollector


class TestMdStatCollector(CollectorTestCase):

    def setUp(self):
        config = get_collector_config('MdStatCollector', {
            'interval': 10
        })

        self.collector = MdStatCollector(config, None)

    def test_import(self):
        self.assertTrue(MdStatCollector)

    @patch('__builtin__.open')
    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_open_proc_loadavg(self, publish_mock, open_mock):
        MdStatCollector.MDSTAT_PATH = '/proc/mdstat'
        if not os.path.exists('/proc/mdstat'):
            # on platforms that don't provide /proc/mdstat: don't bother
            # testing this.
            return
        open_mock.return_value = io.BytesIO('')
        self.collector.collect()
        open_mock.assert_called_once_with('/proc/mdstat', 'r')

    @patch.object(Collector, 'publish')
    def test_mdstat_empty(self, publish_mock):
        MdStatCollector.MDSTAT_PATH = self.getFixturePath('mdstat_empty')
        self.collector.collect()

        metrics = {}

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

    @patch.object(Collector, 'publish')
    def test_mdstat_multiple(self, publish_mock):
        MdStatCollector.MDSTAT_PATH = self.getFixturePath('mdstat_multiple')
        self.collector.collect()

        metrics = {
            'md2.status.superblock_version': 1.2,
            'md2.status.actual_members': 2,
            'md2.status.total_members': 2,
            'md2.status.blocks': 102320,
            'md2.member_count.active': 2,
            'md2.member_count.faulty': 0,
            'md2.member_count.spare': 0,
            'md0.status.total_members': 3,
            'md0.status.blocks': 39058432,
            'md0.status.algorithm': 2,
            'md0.status.superblock_version': 1.2,
            'md0.status.raid_level': 5,
            'md0.status.chunk_size': 524288,
            'md0.status.actual_members': 3,
            'md0.member_count.active': 3,
            'md0.member_count.faulty': 0,
            'md0.member_count.spare': 0,
            'md1.status.superblock_version': 1.2,
            'md1.status.blocks': 199800,
            'md1.status.rounding_factor': 1022976,
            'md1.member_count.active': 2,
            'md1.member_count.faulty': 0,
            'md1.member_count.spare': 0
        }

        self.assertPublishedMany(publish_mock, metrics)

    @patch.object(Collector, 'publish')
    def test_mdstat_linear(self, publish_mock):
        MdStatCollector.MDSTAT_PATH = self.getFixturePath('mdstat_linear')
        self.collector.collect()

        metrics = {
            'md0.status.superblock_version': 1.2,
            'md0.status.blocks': 199800,
            'md0.status.rounding_factor': 1022976,
            'md0.member_count.active': 2,
            'md0.member_count.faulty': 0,
            'md0.member_count.spare': 0
        }

        self.assertPublishedMany(publish_mock, metrics)

    @patch.object(Collector, 'publish')
    def test_mdstat_multipath(self, publish_mock):
        MdStatCollector.MDSTAT_PATH = self.getFixturePath('mdstat_multipath')
        self.collector.collect()

        metrics = {
            'md0.status.superblock_version': 1.2,
            'md0.status.actual_members': 2,
            'md0.status.total_members': 2,
            'md0.status.blocks': 102320,
            'md0.member_count.active': 2,
            'md0.member_count.faulty': 0,
            'md0.member_count.spare': 0
        }

        self.assertPublishedMany(publish_mock, metrics)

    @patch.object(Collector, 'publish')
    def test_mdstat_raid1(self, publish_mock):
        MdStatCollector.MDSTAT_PATH = self.getFixturePath('mdstat_raid1')
        self.collector.collect()

        metrics = {
            'md0.status.superblock_version': 1.2,
            'md0.status.actual_members': 2,
            'md0.status.total_members': 2,
            'md0.status.blocks': 100171776,
            'md0.member_count.active': 2,
            'md0.member_count.faulty': 0,
            'md0.member_count.spare': 0,
            'md0.bitmap.total_pages': 1,
            'md0.bitmap.allocated_pages': 1,
            'md0.bitmap.page_size': 4,
            'md0.bitmap.chunk_size': 65536
        }

        self.assertPublishedMany(publish_mock, metrics)

    @patch.object(Collector, 'publish')
    def test_mdstat_raid1_failed(self, publish_mock):
        MdStatCollector.MDSTAT_PATH = \
            self.getFixturePath('mdstat_raid1-failed')
        self.collector.collect()

        metrics = {
            'md0.status.superblock_version': 1.2,
            'md0.status.actual_members': 1,
            'md0.status.total_members': 2,
            'md0.status.blocks': 102272,
            'md0.member_count.active': 1,
            'md0.member_count.faulty': 1,
            'md0.member_count.spare': 0
        }

        self.assertPublishedMany(publish_mock, metrics)

    @patch.object(Collector, 'publish')
    def test_mdstat_raid1_recover(self, publish_mock):
        MdStatCollector.MDSTAT_PATH = \
            self.getFixturePath('mdstat_raid1-recover')
        self.collector.collect()

        metrics = {
            'md0.status.superblock_version': 1.2,
            'md0.status.actual_members': 1,
            'md0.status.total_members': 2,
            'md0.status.blocks': 102272,
            'md0.recovery.percent': 99.5,
            'md0.recovery.speed': 104726528,
            'md0.recovery.remaining_time': 802199,
            'md0.member_count.active': 2,
            'md0.member_count.faulty': 0,
            'md0.member_count.spare': 0,
            'md0.bitmap.total_pages': 1,
            'md0.bitmap.allocated_pages': 1,
            'md0.bitmap.page_size': 4,
            'md0.bitmap.chunk_size': 65536
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

    @patch.object(Collector, 'publish')
    def test_mdstat_raid1_spare(self, publish_mock):
        MdStatCollector.MDSTAT_PATH = \
            self.getFixturePath('mdstat_raid1-spare')
        self.collector.collect()

        metrics = {
            'md0.status.superblock_version': 1.2,
            'md0.status.actual_members': 2,
            'md0.status.total_members': 2,
            'md0.status.blocks': 100171776,
            'md0.member_count.active': 2,
            'md0.member_count.faulty': 0,
            'md0.member_count.spare': 1,
            'md0.bitmap.total_pages': 1,
            'md0.bitmap.allocated_pages': 1,
            'md0.bitmap.page_size': 4,
            'md0.bitmap.chunk_size': 65536
        }

        self.assertPublishedMany(publish_mock, metrics)

    @patch.object(Collector, 'publish')
    def test_mdstat_raid5(self, publish_mock):
        MdStatCollector.MDSTAT_PATH = \
            self.getFixturePath('mdstat_raid5')
        self.collector.collect()

        metrics = {
            'md0.status.total_members': 3,
            'md0.status.blocks': 39058432,
            'md0.status.algorithm': 2,
            'md0.status.superblock_version': 1.2,
            'md0.status.raid_level': 5,
            'md0.status.chunk_size': 524288,
            'md0.status.actual_members': 3,
            'md0.member_count.active': 3,
            'md0.member_count.faulty': 0,
            'md0.member_count.spare': 0
        }

        self.assertPublishedMany(publish_mock, metrics)

if __name__ == "__main__":
    unittest.main()
