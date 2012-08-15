#!/usr/bin/python
# coding=utf-8
################################################################################

from test import *

from diamond.collector import Collector
from ping import PingCollector

################################################################################

class TestPingCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('PingCollector', {
            'interval': 10,
            'target_a': 'localhost',
            'bin' : 'true'
        })

        self.collector = PingCollector(config, None)

    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data_bad_gentoo(self, publish_mock):
        with patch('subprocess.Popen.communicate', Mock(return_value =
            ( self.getFixture('bad_gentoo').getvalue() , '')
        )):
            self.collector.collect()

        self.assertPublishedMany(publish_mock, {
            'localhost': 10000
        })

    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data_host_gentoo(self, publish_mock):
        with patch('subprocess.Popen.communicate', Mock(return_value =
            ( self.getFixture('host_gentoo').getvalue() , '')
        )):
            self.collector.collect()

        metrics = {
            'localhost': 11
        }
        
        self.setDocExample(self.collector.__class__.__name__, metrics)
        self.assertPublishedMany(publish_mock, metrics)
        
    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data_ip_gentoo(self, publish_mock):
        with patch('subprocess.Popen.communicate', Mock(return_value =
            ( self.getFixture('ip_gentoo').getvalue() , '')
        )):
            self.collector.collect()

        self.assertPublishedMany(publish_mock, {
            'localhost': 0
        })

    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data_longhost_gentoo(self, publish_mock):
        with patch('subprocess.Popen.communicate', Mock(return_value =
            ( self.getFixture('longhost_gentoo').getvalue() , '')
        )):
            self.collector.collect()

        self.assertPublishedMany(publish_mock, {
            'localhost': 10
        })

    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data_timeout_gentoo(self, publish_mock):
        with patch('subprocess.Popen.communicate', Mock(return_value =
            ( self.getFixture('timeout_gentoo').getvalue() , '')
        )):
            self.collector.collect()

        self.assertPublishedMany(publish_mock, {
            'localhost': 10000
        })

    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data_host_osx(self, publish_mock):
        with patch('subprocess.Popen.communicate', Mock(return_value =
            ( self.getFixture('host_osx').getvalue() , '')
        )):
            self.collector.collect()

        self.assertPublishedMany(publish_mock, {
            'localhost': 38
        })
        
    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data_ip_osx(self, publish_mock):
        with patch('subprocess.Popen.communicate', Mock(return_value =
            ( self.getFixture('ip_osx').getvalue() , '')
        )):
            self.collector.collect()

        self.assertPublishedMany(publish_mock, {
            'localhost': 0
        })

    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data_longhost_osx(self, publish_mock):
        with patch('subprocess.Popen.communicate', Mock(return_value =
            ( self.getFixture('longhost_osx').getvalue() , '')
        )):
            self.collector.collect()

        self.assertPublishedMany(publish_mock, {
            'localhost': 42
        })

    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data_timeout_osx(self, publish_mock):
        with patch('subprocess.Popen.communicate', Mock(return_value =
            ( self.getFixture('timeout_osx').getvalue() , '')
        )):
            self.collector.collect()

        self.assertPublishedMany(publish_mock, {
            'localhost': 10000
        })

################################################################################
if __name__ == "__main__":
    unittest.main()
