#!/usr/bin/python
# coding=utf-8
##########################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import Mock
from mock import call
from mock import patch

from diamond.collector import Collector
from smart import SmartCollector

##########################################################################


class TestSmartCollector(CollectorTestCase):

    def setUp(self):
        config = get_collector_config('SmartCollector', {
            'interval': 10,
            'bin': 'true',
            'valtypes': ['value', 'worst', 'thresh', 'raw_val'],
            'attributes': {
                'spin_up_time': True,
                'power_cycle_count': True,
                'temperature_celsius': True,
                'udma_crc_error_count': True,
                '172': True,
                '174': True,
                '234': True},
            'aliases': {
                'disk0': {
                    '172': 'some_attribute',
                    '174': 'and_other_one',
                    '234': 'and_another_one'},
                'sda': {
                    'udma_crc_error_count': 'udma_crc_errs'}},
            'force_prefails': True
        })

        self.collector = SmartCollector(config, None)

    def test_import(self):
        self.assertTrue(SmartCollector)

    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data_osx_missing(self, publish_mock):
        patch_listdir = patch('os.listdir', Mock(return_value=['disk0']))
        patch_communicate = patch(
            'subprocess.Popen.communicate',
            Mock(return_value=(
                self.getFixture('osx_missing').getvalue(),
                '')))
        patch_listdir.start()
        patch_communicate.start()
        self.collector.collect()
        patch_listdir.stop()
        patch_communicate.stop()

        self.assertPublishedMany(publish_mock, {})

    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data_osx_ssd(self, publish_mock):
        patch_listdir = patch('os.listdir', Mock(return_value=['disk0']))
        patch_communicate = patch(
            'subprocess.Popen.communicate',
            Mock(return_value=(
                self.getFixture('osx_ssd').getvalue(),
                '')))
        patch_listdir.start()
        patch_communicate.start()
        self.collector.collect()
        patch_listdir.stop()
        patch_communicate.stop()

        self.assertPublishedMany(publish_mock, {

            # attributes

            'disk0.old_age.power_cycle_count.value': 100,
            'disk0.old_age.power_cycle_count.worst': 100,
            'disk0.old_age.power_cycle_count.thresh': 0,
            'disk0.old_age.power_cycle_count.raw_val': 381,

            'disk0.pre-fail.temperature_celsius.value': 100,
            'disk0.pre-fail.temperature_celsius.worst': 100,
            'disk0.pre-fail.temperature_celsius.thresh': 10,
            'disk0.pre-fail.temperature_celsius.raw_val': 0,

            # value {force_prefails}

            'disk0.pre-fail.head_amplitude.value': 100,
            'disk0.pre-fail.reallocated_sector_ct.value': 100,
            'disk0.pre-fail.raw_read_error_rate.value': 92,

            # worst {force_prefails}

            'disk0.pre-fail.head_amplitude.worst': 100,
            'disk0.pre-fail.reallocated_sector_ct.worst': 100,
            'disk0.pre-fail.raw_read_error_rate.worst': 92,

            # thresh {force_prefails}

            'disk0.pre-fail.head_amplitude.thresh': 000,
            'disk0.pre-fail.reallocated_sector_ct.thresh': 3,
            'disk0.pre-fail.raw_read_error_rate.thresh': 50,

            # raw_val {force_prefails}

            'disk0.pre-fail.head_amplitude.raw_val': 100,
            'disk0.pre-fail.reallocated_sector_ct.raw_val': 0,
            'disk0.pre-fail.raw_read_error_rate.raw_val': 5849487,

            # aliases

            'disk0.old_age.some_attribute.value': 0,
            'disk0.old_age.and_other_one.value': 0,
            'disk0.old_age.and_another_one.value': 0,
            'disk0.old_age.some_attribute.worst': 0,
            'disk0.old_age.and_other_one.worst': 0,
            'disk0.old_age.and_another_one.worst': 0,
            'disk0.old_age.some_attribute.thresh': 0,
            'disk0.old_age.and_other_one.thresh': 0,
            'disk0.old_age.and_another_one.thresh': 0,
            'disk0.old_age.some_attribute.raw_val': 0,
            'disk0.old_age.and_other_one.raw_val': 3,
            'disk0.old_age.and_another_one.raw_val': 2447
        })

    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data_centos55_hdd(self, publish_mock):
        patch_listdir = patch('os.listdir', Mock(return_value=['sda']))
        patch_communicate = patch(
            'subprocess.Popen.communicate',
            Mock(return_value=(
                self.getFixture('centos5.5_hdd').getvalue(),
                '')))

        patch_listdir.start()
        patch_communicate.start()
        self.collector.collect()
        patch_listdir.stop()
        patch_communicate.stop()

        metrics = {

            # attributes

            'sda.pre-fail.spin_up_time.value': 140,
            'sda.pre-fail.spin_up_time.worst': 140,
            'sda.pre-fail.spin_up_time.thresh': 21,
            'sda.pre-fail.spin_up_time.raw_val': 3991,

            'sda.old_age.power_cycle_count.value': 100,
            'sda.old_age.power_cycle_count.worst': 100,
            'sda.old_age.power_cycle_count.thresh': 0,
            'sda.old_age.power_cycle_count.raw_val': 7,

            'sda.old_age.temperature_celsius.value': 115,
            'sda.old_age.temperature_celsius.worst': 110,
            'sda.old_age.temperature_celsius.thresh': 0,
            'sda.old_age.temperature_celsius.raw_val': 28,

            # value {force_prefails}

            'sda.pre-fail.raw_read_error_rate.value': 200,
            'sda.pre-fail.reallocated_sector_ct.value': 200,

            # worst {force_prefails}

            'sda.pre-fail.raw_read_error_rate.worst': 200,
            'sda.pre-fail.reallocated_sector_ct.worst': 200,

            # thresh {force_prefails}

            'sda.pre-fail.raw_read_error_rate.thresh': 51,
            'sda.pre-fail.reallocated_sector_ct.thresh': 140,

            # raw_val {force_prefails}

            'sda.pre-fail.raw_read_error_rate.raw_val': 0,
            'sda.pre-fail.reallocated_sector_ct.raw_val': 0,

            # aliases

            'sda.old_age.udma_crc_errs.value': 200,
            'sda.old_age.udma_crc_errs.worst': 200,
            'sda.old_age.udma_crc_errs.thresh': 0,
            'sda.old_age.udma_crc_errs.raw_val': 0
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data_debian_invalid_checksum_warning(
            self, publish_mock):
        fixture_data = self.getFixture(
            'debian_invalid_checksum_warning').getvalue()
        patch_listdir = patch('os.listdir', Mock(return_value=['sda']))
        patch_communicate = patch('subprocess.Popen.communicate',
                                  Mock(return_value=(fixture_data, '')))

        patch_listdir.start()
        patch_communicate.start()
        self.collector.collect()
        patch_listdir.stop()
        patch_communicate.stop()

        metrics = {

            # attributes

            'sda.pre-fail.spin_up_time.value': 175,
            'sda.pre-fail.spin_up_time.worst': 175,
            'sda.pre-fail.spin_up_time.thresh': 21,
            'sda.pre-fail.spin_up_time.raw_val': 4225,

            'sda.old_age.power_cycle_count.value': 100,
            'sda.old_age.power_cycle_count.worst': 100,
            'sda.old_age.power_cycle_count.thresh': 0,
            'sda.old_age.power_cycle_count.raw_val': 13,

            'sda.old_age.temperature_celsius.value': 112,
            'sda.old_age.temperature_celsius.worst': 111,
            'sda.old_age.temperature_celsius.thresh': 0,
            'sda.old_age.temperature_celsius.raw_val': 35,

            # value {force_prefails}

            'sda.pre-fail.raw_read_error_rate.value': 200,
            'sda.pre-fail.reallocated_sector_ct.value': 200,

            # worst {force_prefails}

            'sda.pre-fail.raw_read_error_rate.worst': 200,
            'sda.pre-fail.reallocated_sector_ct.worst': 200,

            # thresh {force_prefails}

            'sda.pre-fail.raw_read_error_rate.thresh': 51,
            'sda.pre-fail.reallocated_sector_ct.thresh': 140,

            # raw_val {force_prefails}

            'sda.pre-fail.raw_read_error_rate.raw_val': 0,
            'sda.pre-fail.reallocated_sector_ct.raw_val': 0,

            # aliases

            'sda.old_age.udma_crc_errs.value': 200,
            'sda.old_age.udma_crc_errs.worst': 200,
            'sda.old_age.udma_crc_errs.thresh': 0,
            'sda.old_age.udma_crc_errs.raw_val': 0
        }

        header_call = call('sda.ATTRIBUTE_NAME', 'RAW_VALUE')
        published_metric_header = header_call in publish_mock.mock_calls
        assert not published_metric_header, "published metric for header row"

        self.assertPublishedMany(publish_mock, metrics)

    def test_find_attr_start_line(self):
        def get_fixture_lines(fixture):
            return self.getFixture(fixture).getvalue().strip().splitlines()

        def assert_attrs_start_at(expected, fixture):
            lines = get_fixture_lines(fixture)
            self.assertEqual(expected,
                             self.collector.find_attr_start_line(lines))

        lines = get_fixture_lines('osx_missing')
        self.assertEqual(5, self.collector.find_attr_start_line(lines, 2, 4))

        assert_attrs_start_at(7, 'osx_ssd')
        assert_attrs_start_at(7, 'centos5.5_hdd')
        assert_attrs_start_at(8, 'debian_invalid_checksum_warning')

##########################################################################
if __name__ == "__main__":
    unittest.main()
