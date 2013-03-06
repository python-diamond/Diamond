#!/usr/bin/python
# coding=utf-8
################################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import Mock
from mock import call
from mock import patch

from diamond.collector import Collector
from smart import SmartCollector

################################################################################


class TestSmartCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('SmartCollector', {
            'interval': 10,
            'bin': 'true',
        })

        self.collector = SmartCollector(config, None)

    def test_import(self):
        self.assertTrue(SmartCollector)

    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data_osx_missing(self, publish_mock):
        patch_listdir = patch('os.listdir', Mock(return_value=['disk0']))
        patch_communicate = patch('subprocess.Popen.communicate',
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
        patch_communicate = patch('subprocess.Popen.communicate',
                                  Mock(return_value=(
                                    self.getFixture('osx_ssd').getvalue(),
                                    '')))
        patch_listdir.start()
        patch_communicate.start()
        self.collector.collect()
        patch_listdir.stop()
        patch_communicate.stop()

        self.assertPublishedMany(publish_mock, {
            'disk0.172': 0,
            'disk0.Head_Amplitude': 100,
            'disk0.Reallocated_Sector_Ct': 0,
            'disk0.Temperature_Celsius': 128,
            'disk0.174': 3,
            'disk0.Reported_Uncorrect': 0,
            'disk0.Raw_Read_Error_Rate': 5849487,
            'disk0.Power_On_Hours': 199389561752279,
            'disk0.Total_LBAs_Read': 17985,
            'disk0.Power_Cycle_Count': 381,
            'disk0.Hardware_ECC_Recovered': 5849487,
            'disk0.171': 0,
            'disk0.Soft_Read_Error_Rate': 5849487,
            'disk0.234': 2447,
            'disk0.Program_Fail_Cnt_Total': 0,
            'disk0.Media_Wearout_Indicator': 4881,
            'disk0.Erase_Fail_Count_Total': 0,
            'disk0.Wear_Leveling_Count': 2,
            'disk0.Reallocated_Event_Count': 0,
            'disk0.Total_LBAs_Written': 2447,
            'disk0.Soft_ECC_Correction': 5849487,
        })

    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data_centos55_hdd(self, publish_mock):
        patch_listdir = patch('os.listdir', Mock(return_value=['sda']))
        patch_communicate = patch('subprocess.Popen.communicate',
                                  Mock(return_value=(
                                    self.getFixture('centos5.5_hdd').getvalue(),
                                    '')))

        patch_listdir.start()
        patch_communicate.start()
        self.collector.collect()
        patch_listdir.stop()
        patch_communicate.stop()

        metrics = {
            'sda.Temperature_Celsius': 28,
            'sda.Power_On_Hours': 6827,
            'sda.Power_Cycle_Count': 7,
            'sda.Power-Off_Retract_Count': 5,
            'sda.UDMA_CRC_Error_Count': 0,
            'sda.Load_Cycle_Count': 2,
            'sda.Calibration_Retry_Count': 0,
            'sda.Spin_Up_Time': 3991,
            'sda.Spin_Retry_Count': 0,
            'sda.Multi_Zone_Error_Rate': 0,
            'sda.Raw_Read_Error_Rate': 0,
            'sda.Reallocated_Event_Count': 0,
            'sda.Start_Stop_Count': 8,
            'sda.Offline_Uncorrectable': 0,
            'sda.Current_Pending_Sector': 0,
            'sda.Reallocated_Sector_Ct': 0,
            'sda.Seek_Error_Rate': 0,
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data_debian_invalid_checksum_warning(self,
                                                                publish_mock):
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
            'sda.Raw_Read_Error_Rate': 0,
            'sda.Spin_Up_Time': 4225,
            'sda.Start_Stop_Count': 13,
            'sda.Reallocated_Sector_Ct': 0,
            'sda.Seek_Error_Rate': 0,
            'sda.Power_On_Hours': 88,
            'sda.Spin_Retry_Count': 0,
            'sda.Calibration_Retry_Count': 0,
            'sda.Power_Cycle_Count': 13,
            'sda.Power-Off_Retract_Count': 7,
            'sda.Load_Cycle_Count': 5,
            'sda.Temperature_Celsius': 35,
            'sda.Reallocated_Event_Count': 0,
            'sda.Current_Pending_Sector': 0,
            'sda.Offline_Uncorrectable': 0,
            'sda.UDMA_CRC_Error_Count': 0,
            'sda.Multi_Zone_Error_Rate': 0,
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

################################################################################
if __name__ == "__main__":
    unittest.main()
