#!/usr/bin/python
# coding=utf-8
################################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import Mock
from mock import patch

from diamond.collector import Collector
from ping import PingCollector

################################################################################


class TestPingExtendedCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('PingCollector', {
            'interval': 10,
            'target_a': 'localhost',
            'bin': 'true',
            'extended': 'true',
            'count': '10'
        })

        self.collector = PingCollector(config, None)

    def test_import(self):
        self.assertTrue(PingCollector)

    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data_bad_gentoo(self, publish_mock):
        patch_communicate = patch(
            'subprocess.Popen.communicate',
            Mock(return_value=(
                self.getFixture('bad_gentoo').getvalue(),
                '')))

        patch_communicate.start()
        self.collector.collect()
        patch_communicate.stop()

        self.assertPublishedMany(publish_mock, {
            'localhost.min': 0,
            'localhost.max': 0,
            'localhost.avg': 0,
            'localhost.mdev': 0
        })

    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data_host_gentoo(self, publish_mock):
        patch_communicate = patch(
            'subprocess.Popen.communicate',
            Mock(return_value=(
                self.getFixture('host_gentoo').getvalue(),
                '')))

        patch_communicate.start()
        self.collector.collect()
        patch_communicate.stop()

        metrics = {
            'localhost.min': 10.607,
            'localhost.max': 10.607,
            'localhost.avg': 10.607,
            'localhost.mdev': 0.000
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data_ip_gentoo(self, publish_mock):
        patch_communicate = patch(
            'subprocess.Popen.communicate',
            Mock(return_value=(
                self.getFixture('ip_gentoo').getvalue(),
                '')))

        patch_communicate.start()
        self.collector.collect()
        patch_communicate.stop()

        self.assertPublishedMany(publish_mock, {
            'localhost.min': 0.063,
            'localhost.max': 0.063,
            'localhost.avg': 0.063,
            'localhost.mdev': 0.000
        })

    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data_longhost_gentoo(self, publish_mock):
        patch_communicate = patch(
            'subprocess.Popen.communicate',
            Mock(return_value=(
                self.getFixture(
                    'longhost_gentoo').getvalue(),
                '')))

        patch_communicate.start()
        self.collector.collect()
        patch_communicate.stop()

        self.assertPublishedMany(publish_mock, {
            'localhost.min': 10.244,
            'localhost.max': 10.244,
            'localhost.avg': 10.244,
            'localhost.mdev': 0.000
        })

    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data_fasthost_gentoo(self, publish_mock):
        patch_communicate = patch(
            'subprocess.Popen.communicate',
            Mock(return_value=(
                self.getFixture(
                    'fasthost_gentoo').getvalue(),
                '')))

        patch_communicate.start()
        self.collector.collect()
        patch_communicate.stop()

        self.assertPublishedMany(publish_mock, {
            'localhost.min': 0.162,
            'localhost.max': 0.162,
            'localhost.avg': 0.162,
            'localhost.mdev': 0.000
        })

    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data_timeout_gentoo(self, publish_mock):
        patch_communicate = patch(
            'subprocess.Popen.communicate',
            Mock(return_value=(
                self.getFixture(
                    'timeout_gentoo').getvalue(),
                '')))

        patch_communicate.start()
        self.collector.collect()
        patch_communicate.stop()

        self.assertPublishedMany(publish_mock, {
            'localhost.min': 0,
            'localhost.max': 0,
            'localhost.avg': 0,
            'localhost.mdev': 0
        })

    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data_host_osx(self, publish_mock):
        patch_communicate = patch(
            'subprocess.Popen.communicate',
            Mock(return_value=(
                self.getFixture('host_osx').getvalue(),
                '')))

        patch_communicate.start()
        self.collector.collect()
        patch_communicate.stop()

        self.assertPublishedMany(publish_mock, {
            'localhost.min': 38.088,
            'localhost.max': 38.088,
            'localhost.avg': 38.088,
            'localhost.mdev': 0.000
        })

    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data_ip_osx(self, publish_mock):
        patch_communicate = patch(
            'subprocess.Popen.communicate',
            Mock(return_value=(
                self.getFixture('ip_osx').getvalue(),
                '')))

        patch_communicate.start()
        self.collector.collect()
        patch_communicate.stop()

        self.assertPublishedMany(publish_mock, {
            'localhost.min': 0.223,
            'localhost.max': 0.223,
            'localhost.avg': 0.223,
            'localhost.mdev': 0.000
        })

    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data_longhost_osx(self, publish_mock):
        patch_communicate = patch(
            'subprocess.Popen.communicate',
            Mock(return_value=(
                self.getFixture('longhost_osx').getvalue(),
                '')))

        patch_communicate.start()
        self.collector.collect()
        patch_communicate.stop()

        self.assertPublishedMany(publish_mock, {
            'localhost.min': 41.621,
            'localhost.max': 41.621,
            'localhost.avg': 41.621,
            'localhost.mdev': 0.000
        })

    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data_fasthost_osx(self, publish_mock):
        patch_communicate = patch(
            'subprocess.Popen.communicate',
            Mock(return_value=(
                self.getFixture('fasthost_osx').getvalue(),
                '')))

        patch_communicate.start()
        self.collector.collect()
        patch_communicate.stop()

        self.assertPublishedMany(publish_mock, {
            'localhost.min': 0.162,
            'localhost.max': 0.162,
            'localhost.avg': 0.162,
            'localhost.mdev': 0
        })

    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data_timeout_osx(self, publish_mock):
        patch_communicate = patch(
            'subprocess.Popen.communicate',
            Mock(return_value=(
                self.getFixture('timeout_osx').getvalue(),
                '')))

        patch_communicate.start()
        self.collector.collect()
        patch_communicate.stop()

        self.assertPublishedMany(publish_mock, {
            'localhost.min': 0,
            'localhost.max': 0,
            'localhost.avg': 0,
            'localhost.mdev': 0
        })
################################################################################
if __name__ == "__main__":
    unittest.main()
