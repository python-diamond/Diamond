#!/usr/bin/python
################################################################################

from test import *

from diamond.collector import Collector
from smart import SmartCollector

################################################################################

class TestSmartCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('SmartCollector', {
            'interval'  : 10,
            'devices'   : r"^disk[0-9]$|^sd[a-z]$|^hd[a-z]$"
        })

        self.collector = SmartCollector(config, None)
        
    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        
        attributes_1 = [('disk1.1-Raw_Read_Error_Rate',         '146033788962' ),
                        ('disk1.5-Reallocated_Sector_Ct',       '0' ),
                        ('disk1.9-Power_On_Hours',              '93986769339771' ),
                        ('disk1.12-Power_Cycle_Count',          '264' ),
                        ('disk1.171-Unknown_Attribute',         '0' ),
                        ('disk1.172-Unknown_Attribute',         '0' ),
                        ('disk1.174-Unknown_Attribute',         '3' ),
                        ('disk1.177-Wear_Leveling_Count',       '2' ),
                        ('disk1.181-Program_Fail_Cnt_Total',    '0' ),
                        ('disk1.182-Erase_Fail_Count_Total',    '0' ),
                        ('disk1.187-Reported_Uncorrect',        '0' ),
                        ('disk1.194-Temperature_Celsius',       '128' ),
                        ('disk1.195-Hardware_ECC_Recovered',    '146033788962' ),
                        ('disk1.196-Reallocated_Event_Count',   '0' ),
                        ('disk1.201-Soft_Read_Error_Rate',      '146033788962' ),
                        ('disk1.204-Soft_ECC_Correction',       '146033788962' ),
                        ('disk1.230-Head_Amplitude',            '429496729700' ),
                        ('disk1.231-Temperature_Celsius',       '0' ),
                        ('disk1.233-Media_Wearout_Indicator',   '2658' ),
                        ('disk1.234-Unknown_Attribute',         '1352' ),
                        ('disk1.241-Total_LBAs_Written',        '1352' ),
                        ('disk1.242-Total_LBAs_Read',           '16760' )
                       ]
        attributes_2 = [('disk1.1-Raw_Read_Error_Rate',         '146033788972' ),
                        ('disk1.5-Reallocated_Sector_Ct',       '0' ),
                        ('disk1.9-Power_On_Hours',              '93986769339791' ),
                        ('disk1.12-Power_Cycle_Count',          '264' ),
                        ('disk1.171-Unknown_Attribute',         '0' ),
                        ('disk1.172-Unknown_Attribute',         '0' ),
                        ('disk1.174-Unknown_Attribute',         '3' ),
                        ('disk1.177-Wear_Leveling_Count',       '2' ),
                        ('disk1.181-Program_Fail_Cnt_Total',    '0' ),
                        ('disk1.182-Erase_Fail_Count_Total',    '0' ),
                        ('disk1.187-Reported_Uncorrect',        '0' ),
                        ('disk1.194-Temperature_Celsius',       '128' ),
                        ('disk1.195-Hardware_ECC_Recovered',    '146033788992' ),
                        ('disk1.196-Reallocated_Event_Count',   '0' ),
                        ('disk1.201-Soft_Read_Error_Rate',      '146033788972' ),
                        ('disk1.204-Soft_ECC_Correction',       '146033788972' ),
                        ('disk1.230-Head_Amplitude',            '429496729700' ),
                        ('disk1.231-Temperature_Celsius',       '0' ),
                        ('disk1.233-Media_Wearout_Indicator',   '2658' ),
                        ('disk1.234-Unknown_Attribute',         '1352' ),
                        ('disk1.241-Total_LBAs_Written',        '1352' ),
                        ('disk1.242-Total_LBAs_Read',           '16760' )
                       ]
        
        with nested(
            patch.object(SmartCollector, 'getDisks', Mock(return_value = ['disk1'])),
            patch.object(SmartCollector, 'getSmartAttributes', Mock(return_value = attributes_1))
            ):
            self.collector.collect()
        self.assertPublishedMany(publish_mock, {})
        
        with nested(
            patch.object(SmartCollector, 'getDisks', Mock(return_value = ['disk1'])),
            patch.object(SmartCollector, 'getSmartAttributes', Mock(return_value = attributes_2))
            ):
            self.collector.collect()
        
        self.assertPublishedMany(publish_mock, {
                'disk1.1-Raw_Read_Error_Rate'       : 1.0,
                'disk1.5-Reallocated_Sector_Ct'     : 0.0,
                'disk1.9-Power_On_Hours'            : 2.0,
                'disk1.12-Power_Cycle_Count'        : 0.0,
                'disk1.171-Unknown_Attribute'       : 0.0,
                'disk1.172-Unknown_Attribute'       : 0.0,
                'disk1.174-Unknown_Attribute'       : 0.0,
                'disk1.177-Wear_Leveling_Count'     : 0.0,
                'disk1.181-Program_Fail_Cnt_Total'  : 0.0,
                'disk1.182-Erase_Fail_Count_Total'  : 0.0,
                'disk1.187-Reported_Uncorrect'      : 0.0,
                'disk1.194-Temperature_Celsius'     : 0.0,
                'disk1.195-Hardware_ECC_Recovered'  : 3.0,
                'disk1.196-Reallocated_Event_Count' : 0.0,
                'disk1.201-Soft_Read_Error_Rate'    : 1.0,
                'disk1.204-Soft_ECC_Correction'     : 1.0,
                'disk1.230-Head_Amplitude'          : 0.0,
                'disk1.231-Temperature_Celsius'     : 0.0,
                'disk1.233-Media_Wearout_Indicator' : 0.0,
                'disk1.234-Unknown_Attribute'       : 0.0,
                'disk1.241-Total_LBAs_Written'      : 0.0,
                'disk1.242-Total_LBAs_Read'         : 0.0,
            })
        
