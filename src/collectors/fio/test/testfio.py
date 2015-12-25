#!/usr/bin/python
# coding=utf-8

try:
    import json
except ImportError:
    import simplejson as json

import subprocess

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from test import run_only
from mock import patch, call

from diamond.collector import Collector
import fio


def run_only_if_assertSequenceEqual_is_available(func):
    pred = lambda: 'assertSequenceEqual' in dir(unittest.TestCase)
    return run_only(func, pred)


def run_only_if_subprocess_check_output_is_available(func):
    pred = lambda: 'check_output' in dir(subprocess)
    return run_only(func, pred)


class TestCounterIterator(unittest.TestCase):

    @run_only_if_assertSequenceEqual_is_available
    def test_empty(self):
        data = {}
        expected = []
        actual = list(fio.flatten_dictionary(data))
        self.assertSequenceEqual(actual, expected)

    @run_only_if_assertSequenceEqual_is_available
    def test_simple(self):
        data = {'a': '1', 'b': '2'}
        expected = [('a', '1'), ('b', '2')]
        actual = list(fio.flatten_dictionary(data))
        self.assertSequenceEqual(actual, expected)

    @run_only_if_assertSequenceEqual_is_available
    def test_nested(self):
        data = {'a': '1', 'b': '2', 'c': {'d': '3'}}
        expected = [('a', '1'), ('b', '2'), ('c.d', '3')]
        actual = list(fio.flatten_dictionary(data))
        self.assertSequenceEqual(actual, expected)

    @run_only_if_assertSequenceEqual_is_available
    def test_doubly_nested(self):
        data = {'a': 1, 'b': 2, 'c': {'d': 3}, 'e': {'f': {'g': 1}}}
        expected = [('a', 1), ('b', 2), ('c.d', 3), ('e.f.g', 1)]
        actual = list(fio.flatten_dictionary(data))
        self.assertSequenceEqual(actual, expected)


class TestFioCollectorGettingStats(CollectorTestCase):

    def setUp(self):
        config = get_collector_config('FioCollector', {
            'interval': 10,
        })
        self.collector = fio.FioCollector(config, None)

    def test_import(self):
        self.assertTrue(fio.FioCollector)

    @run_only_if_subprocess_check_output_is_available
    @patch('subprocess.check_output')
    def test_load_works(self, check_output):
        expected = {'jobs': [{'a': '1', 'b': '2'}]}
        check_output.return_value = json.dumps(expected)
        actual = self.collector._get_stats_from_fio()
        check_output.assert_called_with(['/usr/bin/fio',
                                         '--name=fio',
                                         '--ioengine=libaio',
                                         '--iodepth=1',
                                         '--rw=readwrite',
                                         '--bs=32k',
                                         '--direct=0',
                                         '--size=100M',
                                         '--numjobs=1',
                                         '--directory=/tmp',
                                         '--output-format=json',
                                         ])
        self.assertEqual(actual, {u'a': u'1', u'b': u'2'})

    @run_only_if_subprocess_check_output_is_available
    @patch('subprocess.check_output')
    def test_fio_command_fails(self, check_output):
        check_output.side_effect = subprocess.CalledProcessError(
            255, ['/usr/bin/fio'], 'error!',
        )
        actual = self.collector._get_stats_from_fio()
        check_output.assert_called_with(['/usr/bin/fio',
                                         '--name=fio',
                                         '--ioengine=libaio',
                                         '--iodepth=1',
                                         '--rw=readwrite',
                                         '--bs=32k',
                                         '--direct=0',
                                         '--size=100M',
                                         '--numjobs=1',
                                         '--directory=/tmp',
                                         '--output-format=json',
                                         ])
        self.assertEqual(actual, {})

    @run_only_if_subprocess_check_output_is_available
    @patch('json.loads')
    @patch('subprocess.check_output')
    def test_json_decode_fails(self, check_output, loads):
        input = {'a': 1,
                 'b': 2,
                 }
        check_output.return_value = json.dumps(input)
        loads.side_effect = ValueError('bad data')
        actual = self.collector._get_stats_from_fio()
        check_output.assert_called_with(['/usr/bin/fio',
                                         '--name=fio',
                                         '--ioengine=libaio',
                                         '--iodepth=1',
                                         '--rw=readwrite',
                                         '--bs=32k',
                                         '--direct=0',
                                         '--size=100M',
                                         '--numjobs=1',
                                         '--directory=/tmp',
                                         '--output-format=json',
                                         ])
        loads.assert_called_with(json.dumps(input))
        self.assertEqual(actual, {})


class TestFioCollectorPublish(CollectorTestCase):

    def setUp(self):
        config = get_collector_config('FioCollector', {
            'interval': 10,
        })
        self.collector = fio.FioCollector(config, None)

    @patch.object(Collector, 'publish')
    def test_simple(self, publish_mock):
        self.collector._publish_stats({'a': '1'})
        publish_mock.assert_called_with('a', '1',
                                        metric_type='GAUGE', instance=None,
                                        precision=0)

    @patch.object(Collector, 'publish')
    def test_multiple(self, publish_mock):
        self.collector._publish_stats({'a': '1', 'b': '2'})
        publish_mock.assert_has_calls([call('a', '1',
                                            metric_type='GAUGE', instance=None,
                                            precision=0),
                                       call('b', '2',
                                            metric_type='GAUGE', instance=None,
                                            precision=0),
                                       ])

if __name__ == "__main__":
    unittest.main()
