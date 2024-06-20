#!/usr/bin/python
# coding=utf-8
################################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import Mock
from mock import patch

from diamond.collector import Collector

from bulk_jolokia import JolokiaBulkCollector

################################################################################


class TestJolokiaBulkCollector(CollectorTestCase):
    def setUp(self):
        c = {'mbeans': ["java.lang:*,type=GarbageCollector"]}
        config = get_collector_config('JolokiaBulkCollector', c)

        self.collector = JolokiaBulkCollector(config, None)

    def test_import(self):
        self.assertTrue(JolokiaBulkCollector)

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        def se(request):
            assert request.get_full_url() == 'http://localhost:8778/jolokia'
            return self.getFixture('multiple_listings')
        patch_urlopen = patch('urllib2.urlopen', Mock(side_effect=se))

        patch_urlopen.start()
        self.collector.collect()
        patch_urlopen.stop()

        metrics = self.get_metrics()
        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

    def test_should_support_basic_auth(self):
        def se(request):
            assert request.has_header('Authorization')

        patch_urlopen = patch('urllib2.urlopen', Mock(side_effect=se))

        authn = {'user': 'x', 'passwd': 'y'}
        config = get_collector_config('JolokiaBulkCollector', authn)
        collector_with_auth = JolokiaBulkCollector(config, None)

        patch_urlopen.start()
        collector_with_auth.open_url("http://localhost:8778")
        patch_urlopen.stop()

    def test_should_support_setting_the_user_agent(self):
        def se(request):
            assert request.has_header('User-agent')
            assert request.get_header('User-agent') == "curl/xyz"

        patch_urlopen = patch('urllib2.urlopen', Mock(side_effect=se))

        ua = {'user-agent': 'curl/xyz'}
        config = get_collector_config('JolokiaBulkCollector', ua)
        collector_with_ua = JolokiaBulkCollector(config, None)

        patch_urlopen.start()
        collector_with_ua.open_url("http://localhost:8778")
        patch_urlopen.stop()

    def get_metrics(self):
        prefix = 'java.lang.name_ParNew.type_GarbageCollector.LastGcInfo'
        return {
            prefix + '.startTime': 14259063,
            prefix + '.id': 219,
            prefix + '.duration': 2,
            prefix + '.memoryUsageBeforeGc.Par_Eden_Space.max': 25165824,
            prefix + '.memoryUsageBeforeGc.Par_Eden_Space.committed': 25165824,
            prefix + '.memoryUsageBeforeGc.Par_Eden_Space.init': 25165824,
            prefix + '.memoryUsageBeforeGc.Par_Eden_Space.used': 25165824,
            prefix + '.memoryUsageBeforeGc.CMS_Old_Gen.max': 73400320,
            prefix + '.memoryUsageBeforeGc.CMS_Old_Gen.committed': 73400320,
            prefix + '.memoryUsageBeforeGc.CMS_Old_Gen.init': 73400320,
            prefix + '.memoryUsageBeforeGc.CMS_Old_Gen.used': 5146840,
            prefix + '.memoryUsageBeforeGc.CMS_Perm_Gen.max': 85983232,
            prefix + '.memoryUsageBeforeGc.CMS_Perm_Gen.committed': 23920640,
            prefix + '.memoryUsageBeforeGc.CMS_Perm_Gen.init': 21757952,
            prefix + '.memoryUsageBeforeGc.CMS_Perm_Gen.used': 23796992,
            prefix + '.memoryUsageBeforeGc.Code_Cache.max': 50331648,
            prefix + '.memoryUsageBeforeGc.Code_Cache.committed': 2686976,
            prefix + '.memoryUsageBeforeGc.Code_Cache.init': 2555904,
            prefix + '.memoryUsageBeforeGc.Code_Cache.used': 2600768,
            prefix + '.memoryUsageBeforeGc.Par_Survivor_Space.max': 3145728,
            prefix + '.memoryUsageBeforeGc.Par_Survivor_Space.committed':
            3145728,
            prefix + '.memoryUsageBeforeGc.Par_Survivor_Space.init': 3145728,
            prefix + '.memoryUsageBeforeGc.Par_Survivor_Space.used': 414088
        }

################################################################################
if __name__ == "__main__":
    unittest.main()
