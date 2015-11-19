#!/usr/bin/python
# coding=utf-8
##########################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import Mock
from mock import patch

from diamond.collector import Collector

from jolokia import JolokiaCollector

##########################################################################


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

        metrics = self.get_metrics()
        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

    @patch.object(Collector, 'publish')
    def test_real_data_with_rewrite(self, publish_mock):
        def se(url):
            if url == 'http://localhost:8778/jolokia/list':
                return self.getFixture('listing')
            else:
                return self.getFixture('stats')
        patch_urlopen = patch('urllib2.urlopen', Mock(side_effect=se))

        patch_urlopen.start()
        self.collector.rewrite = {'memoryUsage': 'memUsed', '.*\.init': ''}
        self.collector.collect()
        patch_urlopen.stop()

        rewritemetrics = self.get_metrics_rewrite_test()
        self.assertPublishedMany(publish_mock, rewritemetrics)

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data_and_basic_auth(self, publish_mock):
        self.collector.config["username"] = "user"
        self.collector.config["password"] = "password"
        self.test_should_work_with_real_data()

    @patch.object(Collector, 'publish')
    def test_should_fail_gracefully(self, publish_mock):
        patch_urlopen = patch('urllib2.urlopen', Mock(
                              return_value=self.getFixture('stats_blank')))

        patch_urlopen.start()
        self.collector.collect()
        patch_urlopen.stop()

        self.assertPublishedMany(publish_mock, {})

    @patch.object(Collector, 'publish')
    def test_should_skip_when_mbean_request_fails(self, publish_mock):
        def se(url):
            if url == 'http://localhost:8778/jolokia/list':
                return self.getFixture('listing_with_bad_mbean')
            elif url == ('http://localhost:8778/jolokia/?ignoreErrors=true'
                         '&p=read/xxx.bad.package:*'):
                return self.getFixture('stats_error')
            else:
                return self.getFixture('stats')
        patch_urlopen = patch('urllib2.urlopen', Mock(side_effect=se))

        patch_urlopen.start()
        self.collector.collect()
        patch_urlopen.stop()

        metrics = self.get_metrics()
        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

    def test_should_escape_jolokia_domains(self):
        domain_with_slash = self.collector.escape_domain('some/domain')
        domain_with_bang = self.collector.escape_domain('some!domain')
        domain_with_quote = self.collector.escape_domain('some"domain')
        self.assertEqual(domain_with_slash, 'some%21/domain')
        self.assertEqual(domain_with_bang, 'some%21%21domain')
        self.assertEqual(domain_with_quote, 'some%21%22domain')

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

    def get_metrics_rewrite_test(self):
        prefix = 'java.lang.name_ParNew.type_GarbageCollector.LastGcInfo'
        return {
            prefix + '.startTime': 14259063,
            prefix + '.id': 219,
            prefix + '.duration': 2,
            prefix + '.memUsedBeforeGc.Par_Eden_Space.max': 25165824,
            prefix + '.memUsedBeforeGc.Par_Eden_Space.committed': 25165824,
            prefix + '.memUsedBeforeGc.Par_Eden_Space.used': 25165824,
            prefix + '.memUsedBeforeGc.CMS_Old_Gen.max': 73400320,
            prefix + '.memUsedBeforeGc.CMS_Old_Gen.committed': 73400320,
            prefix + '.memUsedBeforeGc.CMS_Old_Gen.used': 5146840,
            prefix + '.memUsedBeforeGc.CMS_Perm_Gen.max': 85983232,
            prefix + '.memUsedBeforeGc.CMS_Perm_Gen.committed': 23920640,
            prefix + '.memUsedBeforeGc.CMS_Perm_Gen.used': 23796992,
            prefix + '.memUsedBeforeGc.Code_Cache.max': 50331648,
            prefix + '.memUsedBeforeGc.Code_Cache.committed': 2686976,
            prefix + '.memUsedBeforeGc.Code_Cache.used': 2600768,
            prefix + '.memUsedBeforeGc.Par_Survivor_Space.max': 3145728,
            prefix + '.memUsedBeforeGc.Par_Survivor_Space.committed': 3145728,
            prefix + '.memUsedBeforeGc.Par_Survivor_Space.used': 414088
        }

##########################################################################
if __name__ == "__main__":
    unittest.main()
