#!/usr/bin/python
# coding=utf-8
################################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import Mock
from mock import patch

from diamond.collector import Collector

from jolokia import JolokiaCollector

################################################################################

class TestJolokiaCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('JolokiaCollector', {})

        self.collector = JolokiaCollector(config, None)

    def test_import(self):
        self.assertTrue(JolokiaCollector)

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        def se(url):
            if url == 'http://localhost:8778/jolokia/list':
                return self.getFixture('listing')
            else:
                return self.getFixture('stats')
        patch_urlopen = patch('urllib2.urlopen', Mock(side_effect=se))

        patch_urlopen.start()
        self.collector.collect()
        patch_urlopen.stop()

        metrics = {
            'java.lang.name_ParNew.type_GarbageCollector.LastGcInfo.startTime': 14259063,
            'java.lang.name_ParNew.type_GarbageCollector.LastGcInfo.id': 219,
            'java.lang.name_ParNew.type_GarbageCollector.LastGcInfo.duration': 2,
            'java.lang.name_ParNew.type_GarbageCollector.LastGcInfo.memoryUsageBeforeGc.Par_Eden_Space.max': 25165824,
            'java.lang.name_ParNew.type_GarbageCollector.LastGcInfo.memoryUsageBeforeGc.Par_Eden_Space.committed': 25165824,
            'java.lang.name_ParNew.type_GarbageCollector.LastGcInfo.memoryUsageBeforeGc.Par_Eden_Space.init': 25165824,
            'java.lang.name_ParNew.type_GarbageCollector.LastGcInfo.memoryUsageBeforeGc.Par_Eden_Space.used': 25165824,
            'java.lang.name_ParNew.type_GarbageCollector.LastGcInfo.memoryUsageBeforeGc.CMS_Old_Gen.max': 73400320,
            'java.lang.name_ParNew.type_GarbageCollector.LastGcInfo.memoryUsageBeforeGc.CMS_Old_Gen.committed': 73400320,
            'java.lang.name_ParNew.type_GarbageCollector.LastGcInfo.memoryUsageBeforeGc.CMS_Old_Gen.init': 73400320,
            'java.lang.name_ParNew.type_GarbageCollector.LastGcInfo.memoryUsageBeforeGc.CMS_Old_Gen.used': 5146840,
            'java.lang.name_ParNew.type_GarbageCollector.LastGcInfo.memoryUsageBeforeGc.CMS_Perm_Gen.max': 85983232,
            'java.lang.name_ParNew.type_GarbageCollector.LastGcInfo.memoryUsageBeforeGc.CMS_Perm_Gen.committed': 23920640,
            'java.lang.name_ParNew.type_GarbageCollector.LastGcInfo.memoryUsageBeforeGc.CMS_Perm_Gen.init': 21757952,
            'java.lang.name_ParNew.type_GarbageCollector.LastGcInfo.memoryUsageBeforeGc.CMS_Perm_Gen.used': 23796992,
            'java.lang.name_ParNew.type_GarbageCollector.LastGcInfo.memoryUsageBeforeGc.Code_Cache.max': 50331648,
            'java.lang.name_ParNew.type_GarbageCollector.LastGcInfo.memoryUsageBeforeGc.Code_Cache.committed': 2686976,
            'java.lang.name_ParNew.type_GarbageCollector.LastGcInfo.memoryUsageBeforeGc.Code_Cache.init': 2555904,
            'java.lang.name_ParNew.type_GarbageCollector.LastGcInfo.memoryUsageBeforeGc.Code_Cache.used': 2600768,
            'java.lang.name_ParNew.type_GarbageCollector.LastGcInfo.memoryUsageBeforeGc.Par_Survivor_Space.max': 3145728,
            'java.lang.name_ParNew.type_GarbageCollector.LastGcInfo.memoryUsageBeforeGc.Par_Survivor_Space.committed': 3145728,
            'java.lang.name_ParNew.type_GarbageCollector.LastGcInfo.memoryUsageBeforeGc.Par_Survivor_Space.init': 3145728,
            'java.lang.name_ParNew.type_GarbageCollector.LastGcInfo.memoryUsageBeforeGc.Par_Survivor_Space.used': 414088
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics, 
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

    @patch.object(Collector, 'publish')
    def test_should_fail_gracefully(self, publish_mock):
        patch_urlopen = patch('urllib2.urlopen', Mock(
                              return_value=self.getFixture('stats_blank')))

        patch_urlopen.start()
        self.collector.collect()
        patch_urlopen.stop()

        self.assertPublishedMany(publish_mock, {})

################################################################################
if __name__ == "__main__":
    unittest.main()
