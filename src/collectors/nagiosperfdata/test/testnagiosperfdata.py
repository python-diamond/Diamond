#!/usr/bin/python
# coding=utf-8

from test import CollectorTestCase
from test import get_collector_config
from mock import patch
import os

from diamond.collector import Collector
from nagiosperfdata import NagiosPerfdataCollector


class TestNagiosPerfdataCollector(CollectorTestCase):
    def setUp(self):
        """Set up the fixtures for the test
        """
        fixtures_dir = os.path.abspath(os.path.join(
                os.path.dirname(__file__), 'fixtures'))

        config = get_collector_config('NagiosPerfdataCollector', {
            'perfdata_dir': fixtures_dir
        })

        self.collector = NagiosPerfdataCollector(config, None)
        self.fixtures = os.listdir(fixtures_dir)

    def test_import(self):
        """Test that import works correctly
        """
        self.assertTrue(NagiosPerfdataCollector)

    @patch.object(NagiosPerfdataCollector, '_process_file')
    def test_collect_should_list_fixtures(self, process_mock):
        """Test that collect() finds our test fixtures
        """
        self.collector.collect()
        self.assertTrue(process_mock.called)

    def test_extract_fields_should_extract_fields(self):
        """Test that extract_fields() actually extracts fields
        """
        s = "KEY1::VALUE1\tKEY2::VALUE2 KEY3::VALUE3"
        fields = self.collector._extract_fields(s)
        self.assertEqual(fields.get('KEY1'), 'VALUE1')
        self.assertFalse('KEY2' in fields)

    def test_fields_valid_should_not_validate_invalid_datatype(self):
        fields = {'DATATYPE': 'BAD HOSTPERFDATA',
                  'HOSTNAME': 'testhost',
                  'HOSTPERFDATA': '',
                  'TIMET': 5304577351}
        self.assertFalse(self.collector._fields_valid(fields))

    def test_fields_valid_should_validate_complete_host_fields(self):
        fields = {'DATATYPE': 'HOSTPERFDATA',
                  'HOSTNAME': 'testhost',
                  'HOSTPERFDATA': '',
                  'TIMET': 5304577351}
        self.assertTrue(self.collector._fields_valid(fields))

    def test_fields_valid_should_not_validate_incomplete_host_fields(self):
        fields = {'DATATYPE': 'HOSTPERFDATA',
                  'HOSTNAME': 'testhost',
                  'TIMET': 5304577351}
        self.assertFalse(self.collector._fields_valid(fields))

    def test_fields_valid_should_validate_complete_service_fields(self):
        fields = {'DATATYPE': 'SERVICEPERFDATA',
                  'HOSTNAME': 'testhost',
                  'TIMET': 5304577351,
                  'SERVICEDESC': 'Ping',
                  'SERVICEPERFDATA': ''}
        self.assertTrue(self.collector._fields_valid(fields))

    def test_fields_valid_should_not_validate_incomplete_service_fields(self):
        fields = {'DATATYPE': 'SERVICEPERFDATA',
                  'HOSTNAME': 'testhost',
                  'TIMET': 5304577351,
                  'SERVICEDESC': 'Ping'}
        self.assertFalse(self.collector._fields_valid(fields))

    def test_normalize_to_unit_should_normalize(self):
        self.assertEqual(self.collector._normalize_to_unit(1, None), 1.0)
        self.assertEqual(self.collector._normalize_to_unit(1, 'KB'), 1024.0)

    def test_parse_perfdata_should_parse_valid_perfdata(self):
        perf = self.collector._parse_perfdata(
                'rta=0.325ms;300.000;500.000;0; pl=0%;20;60;;')
        expected_result = [('rta', 0.000325), ('pl', 0.0)]
        self.assertEqual(perf, expected_result)

    def test_parse_perfdata_should_not_parse_invalid_perfdata(self):
        perf = self.collector._parse_perfdata(
            'something with spaces=0.325ms;300.000;500.000;0; pl=0%;20;60;;')
        unexpected_result = [('something with spaces', 0.000325), ('pl', 0.0)]
        self.assertNotEqual(perf, unexpected_result)

    @patch('os.remove')
    @patch.object(Collector, 'publish')
    def test_process_file_should_work_with_real_host_perfdata(self,
            publish_mock, remove_mock):
        path = self.getFixturePath('host-perfdata.0')
        self.collector._process_file(path)
        expected = {
            'nagios.testhost.host.pl': 0,
            'nagios.testhost.host.rta': 0.000325
        }
        self.assertPublishedMany(publish_mock, expected)

    @patch('os.remove')
    @patch.object(Collector, 'publish')
    def test_process_file_should_work_with_real_service_perfdata(self,
            publish_mock, remove_mock):
        path = self.getFixturePath('service-perfdata.0')
        self.collector._process_file(path)
        publish_mock.assert_called_once()

    def test_sanitize_should_sanitize(self):
        orig1 = 'myhost.mydomain'
        sani1 = self.collector._sanitize(orig1)
        self.assertEqual(sani1, 'myhost_mydomain')

        orig2 = '/test/path'
        sani2 = self.collector._sanitize(orig2)
        self.assertEqual(sani2, '_test_path')
