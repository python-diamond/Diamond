#!/usr/bin/python
# coding=utf-8
###############################################################################

from test import CollectorTestCase
from test import get_collector_config
from mock import Mock
from mock import patch

from diamond.collector import Collector
from disktemp import DiskTemperatureCollector

###############################################################################


class TestDiskTemperatureCollector(CollectorTestCase):

    def setUp(self):
        config = get_collector_config('DiskTemperatureCollector', {
            'interval': 10,
            'bin': 'true',
        })

        self.collector = DiskTemperatureCollector(config, None)

    def test_import(self):
        self.assertTrue(DiskTemperatureCollector)

    @patch.object(Collector, 'publish')
    def test_smart_available(self, publish_mock):
        patch_listdir = patch('os.listdir', Mock(return_value=['sda']))
        patch_communicate = patch(
            'subprocess.Popen.communicate',
            Mock(return_value=(
                self.getFixture('hddtemp').getvalue(),
                '')))

        patch_listdir.start()
        patch_communicate.start()
        self.collector.collect()
        patch_listdir.stop()
        patch_communicate.stop()

        self.assertPublished(publish_mock, 'sda.Temperature', 50)

    @patch.object(Collector, 'publish')
    def test_smart_unavailable(self, publish_mock):
        patch_listdir = patch('os.listdir', Mock(return_value=['sda']))
        patch_communicate = patch(
            'subprocess.Popen.communicate',
            Mock(return_value=(
                self.getFixture('smart_missing').getvalue(),
                '')))

        patch_listdir.start()
        patch_communicate.start()
        self.collector.collect()
        patch_listdir.stop()
        patch_communicate.stop()

        self.assertUnpublished(publish_mock, 'sda.Temperature', 50)

    @patch.object(Collector, 'publish')
    def test_filter(self, publish_mock):
        self.collector.config['devices'] = 'sda'
        self.collector.process_config()

        patch_listdir = patch('os.listdir', Mock(return_value=['sda', 'sdb']))
        patch_communicate = patch(
            'subprocess.Popen.communicate',
            Mock(return_value=(
                self.getFixture('hddtemp').getvalue(),
                '')))

        patch_listdir.start()
        patch_communicate.start()
        self.collector.collect()
        patch_listdir.stop()
        patch_communicate.stop()

        self.assertPublished(publish_mock, 'sda.Temperature', 50)
        self.assertUnpublished(publish_mock, 'sdb.Temperature', 50)

    @patch.object(Collector, 'publish')
    def test_regex(self, publish_mock):
        self.collector.config['devices'] = '(s)d(a)'
        self.collector.process_config()

        patch_listdir = patch('os.listdir', Mock(return_value=['sda']))
        patch_communicate = patch(
            'subprocess.Popen.communicate',
            Mock(return_value=(
                self.getFixture('hddtemp').getvalue(),
                '')))

        patch_listdir.start()
        patch_communicate.start()
        self.collector.collect()
        patch_listdir.stop()
        patch_communicate.stop()

        self.assertPublished(publish_mock, 's.a.Temperature', 50)
