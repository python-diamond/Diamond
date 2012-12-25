#!/usr/bin/python
# coding=utf-8

try:
    import json
    json  # workaround for pyflakes issue #13
except ImportError:
    import simplejson as json

import subprocess

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import Mock
from mock import patch
from mock import call

import ceph


def run_only(func, predicate):
    if predicate():
        return func
    else:
        def f(arg):
            pass
        return f


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
        actual = list(ceph.flatten_dictionary(data))
        self.assertSequenceEqual(actual, expected)

    @run_only_if_assertSequenceEqual_is_available
    def test_simple(self):
        data = {'a': 1, 'b': 2}
        expected = [('a', 1), ('b', 2)]
        actual = list(ceph.flatten_dictionary(data))
        self.assertSequenceEqual(actual, expected)

    @run_only_if_assertSequenceEqual_is_available
    def test_prefix(self):
        data = {'a': 1, 'b': 2}
        expected = [('Z.a', 1), ('Z.b', 2)]
        actual = list(ceph.flatten_dictionary(data, prefix='Z'))
        self.assertSequenceEqual(actual, expected)

    @run_only_if_assertSequenceEqual_is_available
    def test_sep(self):
        data = {'a': 1, 'b': 2}
        expected = [('Z:a', 1), ('Z:b', 2)]
        actual = list(ceph.flatten_dictionary(data, prefix='Z', sep=':'))
        self.assertSequenceEqual(actual, expected)

    @run_only_if_assertSequenceEqual_is_available
    def test_nested(self):
        data = {'a': 1, 'b': 2, 'c': {'d': 3}}
        expected = [('a', 1), ('b', 2), ('c.d', 3)]
        actual = list(ceph.flatten_dictionary(data))
        self.assertSequenceEqual(actual, expected)

    @run_only_if_assertSequenceEqual_is_available
    def test_doubly_nested(self):
        data = {'a': 1, 'b': 2, 'c': {'d': 3}, 'e': {'f': {'g': 1}}}
        expected = [('a', 1), ('b', 2), ('c.d', 3), ('e.f.g', 1)]
        actual = list(ceph.flatten_dictionary(data))
        self.assertSequenceEqual(actual, expected)

    @run_only_if_assertSequenceEqual_is_available
    def test_complex(self):
        data = {"val": 0,
                "max": 524288000,
                "get": 60910,
                "wait": {"avgcount": 0,
                         "sum": 0},
                }
        expected = [
            ('get', 60910),
            ('max', 524288000),
            ('val', 0),
            ('wait.avgcount', 0),
            ('wait.sum', 0),
        ]
        actual = list(ceph.flatten_dictionary(data))
        self.assertSequenceEqual(actual, expected)


class TestCephCollectorSocketNameHandling(CollectorTestCase):

    def setUp(self):
        config = get_collector_config('CephCollector', {
            'interval': 10,
        })
        self.collector = ceph.CephCollector(config, None)

    def test_counter_default_prefix(self):
        expected = 'ceph.osd.325'
        sock = '/var/run/ceph/ceph-osd.325.asok'
        actual = self.collector._get_counter_prefix_from_socket_name(sock)
        self.assertEquals(actual, expected)

    def test_counter_alternate_prefix(self):
        expected = 'ceph.keep-osd.325'
        sock = '/var/run/ceph/keep-osd.325.asok'
        actual = self.collector._get_counter_prefix_from_socket_name(sock)
        self.assertEquals(actual, expected)

    def test_get_socket_paths(self):
        config = get_collector_config('CephCollector', {
            'socket_path': '/path/',
            'socket_prefix': 'prefix-',
            'socket_ext': 'ext',
        })
        collector = ceph.CephCollector(config, None)
        glob_mock = patch('glob.glob', Mock(return_value=False))
        gmock = glob_mock.start()
        collector._get_socket_paths()
        glob_mock.stop()
        gmock.assert_called_with('/path/prefix-*.ext')


class TestCephCollectorGettingStats(CollectorTestCase):

    def setUp(self):
        config = get_collector_config('CephCollector', {
            'interval': 10,
        })
        self.collector = ceph.CephCollector(config, None)

    @run_only_if_subprocess_check_output_is_available
    def test_load_works(self):
        expected = {'a': 1,
                    'b': 2,
                    }
        check_output = patch('subprocess.check_output')
        check_output.return_value = json.dumps(expected)
        comock = check_output.start()
        actual = self.collector._get_stats_from_socket('a_socket_name')
        comock.assert_called_with(['/usr/bin/ceph',
                                   '--admin-daemon',
                                   'a_socket_name',
                                   'perf',
                                   'dump',
                                   ])
        self.assertEqual(actual, expected)

    @run_only_if_subprocess_check_output_is_available
    def test_ceph_command_fails(self):
        check_output = patch('subprocess.check_output')
        check_output.side_effect = subprocess.CalledProcessError(
            255, ['/usr/bin/ceph'], 'error!',
        )
        comock = check_output.start()
        actual = self.collector._get_stats_from_socket('a_socket_name')
        comock.assert_called_with(['/usr/bin/ceph',
                                   '--admin-daemon',
                                   'a_socket_name',
                                   'perf',
                                   'dump',
                                   ])
        self.assertEqual(actual, {})

    @run_only_if_subprocess_check_output_is_available
    def test_json_decode_fails(self):
        input = {'a': 1,
                 'b': 2,
                 }
        check_output = patch('subprocess.check_output')
        check_output.return_value = json.dumps(input)
        comock = check_output.start()
        loads = patch('json.loads')
        loads.side_effect = ValueError('bad data')
        loads_mock = loads.start()
        actual = self.collector._get_stats_from_socket('a_socket_name')
        comock.assert_called_with(['/usr/bin/ceph',
                                   '--admin-daemon',
                                   'a_socket_name',
                                   'perf',
                                   'dump',
                                   ])
        loads_mock.assert_called_with(json.dumps(input))
        self.assertEqual(actual, {})


class TestCephCollectorPublish(CollectorTestCase):

    def setUp(self):
        config = get_collector_config('CephCollector', {
            'interval': 10,
        })
        self.collector = ceph.CephCollector(config, None)

    def test_simple(self):
        publish = patch.object(self.collector, 'publish')
        publish_mock = publish.start()
        self.collector._publish_stats('prefix', {'a': 1})
        publish_mock.assert_called_with('prefix.a', 1)

    def test_multiple(self):
        publish = patch.object(self.collector, 'publish')
        publish_mock = publish.start()
        self.collector._publish_stats('prefix', {'a': 1, 'b': 2})
        publish_mock.assert_has_calls([call('prefix.a', 1),
                                       call('prefix.b', 2),
                                       ])

if __name__ == "__main__":
    unittest.main()
