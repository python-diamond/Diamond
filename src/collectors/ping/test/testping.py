#!/usr/bin/python
# coding=utf-8
##########################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from test import Mock
from test import patch

from diamond.collector import Collector
from ping import PingCollector

##########################################################################


class TestPingCollector(CollectorTestCase):

    def setUp(self):
        config = get_collector_config('PingCollector', {
            'interval': 10,
            'target_a': 'localhost',
            'bin': 'true'
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
            'localhost': 10000
        })

    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data_host_gentoo(self, publish_mock):
        config = get_collector_config('PingCollector', {
            'interval': 10,
            'target_a': 'localhost',
            'target_b': 'www.example.org',
            'target_c': '192.168.0.1',
            'bin': 'true'
        })

        collector = PingCollector(config, None)

        def popen_se(command, **kwargs):
            popen_mock = Mock()
            if command[-1] == 'localhost':
                popen_mock.communicate = Mock(return_value=(
                    self.getFixture('host_gentoo').getvalue(),
                    ''))
            elif command[-1] == 'www.example.org':
                popen_mock.communicate = Mock(return_value=(
                    self.getFixture('host_gentoo2').getvalue(),
                    ''))
            elif command[-1] == '192.168.0.1':
                popen_mock.communicate = Mock(return_value=(
                    self.getFixture('host_gentoo3').getvalue(),
                    ''))
            return popen_mock

        patch_popen = patch(
            'subprocess.Popen',
            Mock(side_effect=popen_se))

        patch_popen.start()
        collector.collect()
        patch_popen.stop()

        metrics = {
            'localhost': 11,
            'www_example_org': 23,
            '192_168_0_1': 16
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
            'localhost': 0
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
            'localhost': 10
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
            'localhost': 10000
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
            'localhost': 38
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
            'localhost': 0
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
            'localhost': 42
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
            'localhost': 10000
        })

##########################################################################
if __name__ == "__main__":
    unittest.main()
