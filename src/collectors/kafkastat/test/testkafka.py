#!/usr/bin/python
# coding=utf-8
###############################################################################
import urllib2
from urlparse import urlparse, parse_qs

try:
    from xml.etree import ElementTree
except ImportError:
    ElementTree = None

from test import CollectorTestCase
from test import get_collector_config
from test import run_only
from test import unittest
from mock import patch

from diamond.collector import Collector
from kafkastat import KafkaCollector

##########


def run_only_if_ElementTree_is_available(func):
    try:
        from xml.etree import ElementTree
    except ImportError:
        ElementTree = None

    def pred():
        return ElementTree is not None
    return run_only(func, pred)


class TestKafkaCollector(CollectorTestCase):

    def setUp(self):
        config = get_collector_config('KafkaCollector', {
            'interval': 10
        })

        self.collector = KafkaCollector(config, None)

    def _get_xml_fixture(self, name):
        fixture = self.getFixture(name)

        return ElementTree.fromstring(fixture.getvalue())

    def test_import(self):
        self.assertTrue(KafkaCollector)

    @run_only_if_ElementTree_is_available
    @patch('urllib2.urlopen')
    def test_get(self, urlopen_mock):
        urlopen_mock.return_value = self.getFixture('empty.xml')

        result = self.collector._get('/path')
        result_string = ElementTree.tostring(result)

        self.assertEqual(result_string, '<Server />')

    @run_only_if_ElementTree_is_available
    @patch('urllib2.urlopen')
    def test_get_httperror(self, urlopen_mock):
        urlopen_mock.side_effect = urllib2.URLError('BOOM')

        result = self.collector._get('/path')

        self.assertFalse(result)

    @run_only_if_ElementTree_is_available
    @patch('urllib2.urlopen')
    def test_get_bad_xml(self, urlopen_mock):
        urlopen_mock.return_value = self.getFixture('bad.xml')

        result = self.collector._get('/path')

        self.assertFalse(result)

    @run_only_if_ElementTree_is_available
    @patch.object(KafkaCollector, '_get')
    def test_get_mbeans(self, get_mock):
        get_mock.return_value = self._get_xml_fixture('serverbydomain.xml')

        expected_names = {'kafka:type=kafka.BrokerAllTopicStat',
                          'kafka:type=kafka.BrokerTopicStat.mytopic',
                          'kafka:type=kafka.LogFlushStats',
                          'kafka:type=kafka.SocketServerStats',
                          'kafka:type=kafka.logs.mytopic-0',
                          'kafka:type=kafka.logs.mytopic-1',
                          'kafka:type=kafka.Log4jController'}

        found_beans = self.collector.get_mbeans('*')

        self.assertEqual(found_beans, expected_names)

    @run_only_if_ElementTree_is_available
    @patch.object(KafkaCollector, '_get')
    def test_get_mbeans_get_fail(self, get_mock):
        get_mock.return_value = None

        found_beans = self.collector.get_mbeans('*')

        self.assertEqual(found_beans, None)

    @run_only_if_ElementTree_is_available
    @patch.object(KafkaCollector, '_get')
    def test_query_mbean(self, get_mock):
        get_mock.return_value = self._get_xml_fixture('mbean.xml')

        expected_metrics = {
            'kafka.logs.mytopic-1.CurrentOffset': long('213500615'),
            'kafka.logs.mytopic-1.NumAppendedMessages': long('224634137'),
            'kafka.logs.mytopic-1.NumberOfSegments': int('94'),
            'kafka.logs.mytopic-1.Size': long('50143615339'),
        }

        metrics = self.collector.query_mbean('kafka:type=kafka.logs.mytopic-1')

        self.assertEqual(metrics, expected_metrics)

    @run_only_if_ElementTree_is_available
    @patch.object(KafkaCollector, '_get')
    def test_query_mbean_with_prefix(self, get_mock):
        get_mock.return_value = self._get_xml_fixture('mbean.xml')

        expected_metrics = {
            'some.prefix.CurrentOffset': long('213500615'),
            'some.prefix.NumAppendedMessages': long('224634137'),
            'some.prefix.NumberOfSegments': int('94'),
            'some.prefix.Size': long('50143615339'),
        }

        metrics = self.collector.query_mbean('kafka:type=kafka.logs.mytopic-0',
                                             'some.prefix')

        self.assertEqual(metrics, expected_metrics)

    @run_only_if_ElementTree_is_available
    @patch.object(KafkaCollector, '_get')
    def test_activeController_value(self, get_mock):
        get_mock.return_value = self._get_xml_fixture(
            'activecontrollercount.xml')

        expected_metrics = {
            'KafkaController.ActiveControllerCount.Value': 1.0,
        }

        metrics = self.collector.query_mbean(
            'kafka.controller:type=KafkaController,name=ActiveControllerCount')

        self.assertEqual(metrics, expected_metrics)

    @run_only_if_ElementTree_is_available
    @patch.object(KafkaCollector, '_get')
    def test_query_mbean_fail(self, get_mock):
        get_mock.return_value = None

        metrics = self.collector.query_mbean('kafka:type=kafka.logs.mytopic-0')

        self.assertEqual(metrics, None)

    def getKafkaFixture(self, url):
        url_object = urlparse(url)
        query_string = parse_qs(url_object.query)
        querynames = query_string.get('querynames', [])
        objectnames = query_string.get('objectname', [])

        if url_object.path == '/serverbydomain':
            if 'java.lang:type=GarbageCollector,name=*' in querynames:
                return self.getFixture('serverbydomain_gc.xml')
            elif '*kafka.controller:*' in querynames:
                return self.getFixture('kafkacontroller.xml')
            elif 'java.lang:type=Threading' in querynames:
                return self.getFixture('serverbydomain_threading.xml')
            else:
                return self.getFixture('serverbydomain_logs_only.xml')
        elif url_object.path == '/mbean':
            if ('java.lang:type=GarbageCollector,name=PS MarkSweep'
                    in objectnames):
                return self.getFixture('gc_marksweep.xml')
            elif ('kafka.controller:type=KafkaController,' +
                  'name=ActiveControllerCount'
                  in objectnames):
                return self.getFixture('activecontrollercount.xml')
            elif ('java.lang:type=GarbageCollector,name=PS Scavenge'
                  in objectnames):
                return self.getFixture('gc_scavenge.xml')
            elif 'java.lang:type=Threading' in objectnames:
                return self.getFixture('threading.xml')
            else:
                return self.getFixture('mbean.xml')
        else:
            return ''

    @run_only_if_ElementTree_is_available
    @patch('urllib2.urlopen')
    @patch.object(Collector, 'publish')
    def test(self, publish_mock, urlopen_mock):
        urlopen_mock.side_effect = self.getKafkaFixture

        self.collector.collect()

        expected_metrics = {
            'kafka.logs.mytopic-1.CurrentOffset': 213500615,
            'kafka.logs.mytopic-1.NumAppendedMessages': 224634137,
            'kafka.logs.mytopic-1.NumberOfSegments': 94,
            'kafka.logs.mytopic-1.Size': 50143615339,
            'Threading.CurrentThreadCpuTime': 0,
            'Threading.CurrentThreadUserTime': 0,
            'Threading.DaemonThreadCount': 58,
            'Threading.PeakThreadCount': 90,
            'Threading.ThreadCount': 89,
            'Threading.TotalStartedThreadCount': 228,
            'GarbageCollector.PSScavenge.CollectionCount': 37577,
            'GarbageCollector.PSScavenge.CollectionTime': 112293,
            'GarbageCollector.PSMarkSweep.CollectionCount': 2,
            'GarbageCollector.PSMarkSweep.CollectionTime': 160,
        }

        self.assertPublishedMany(publish_mock, expected_metrics)


###############################################################################
if __name__ == "__main__":
    unittest.main()
