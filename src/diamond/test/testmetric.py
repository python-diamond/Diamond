#!/usr/bin/python
# coding=utf-8
##########################################################################

from test import unittest

from diamond.metric import Metric


class TestMetric(unittest.TestCase):

    def testgetPathPrefix(self):
        metric = Metric('servers.com.example.www.cpu.total.idle',
                        0,
                        host='com.example.www')

        actual_value = metric.getPathPrefix()
        expected_value = 'servers'

        message = 'Actual %s, expected %s' % (actual_value, expected_value)
        self.assertEqual(actual_value, expected_value, message)

    def testgetPathPrefixCustom(self):
        metric = Metric('custom.path.prefix.com.example.www.cpu.total.idle',
                        0,
                        host='com.example.www')

        actual_value = metric.getPathPrefix()
        expected_value = 'custom.path.prefix'

        message = 'Actual %s, expected %s' % (actual_value, expected_value)
        self.assertEqual(actual_value, expected_value, message)

    def testgetCollectorPath(self):
        metric = Metric('servers.com.example.www.cpu.total.idle',
                        0,
                        host='com.example.www')

        actual_value = metric.getCollectorPath()
        expected_value = 'cpu'

        message = 'Actual %s, expected %s' % (actual_value, expected_value)
        self.assertEqual(actual_value, expected_value, message)

    def testgetMetricPath(self):
        metric = Metric('servers.com.example.www.cpu.total.idle',
                        0,
                        host='com.example.www')

        actual_value = metric.getMetricPath()
        expected_value = 'total.idle'

        message = 'Actual %s, expected %s' % (actual_value, expected_value)
        self.assertEqual(actual_value, expected_value, message)

    # Test hostname of none
    def testgetPathPrefixHostNone(self):
        metric = Metric('servers.host.cpu.total.idle',
                        0)

        actual_value = metric.getPathPrefix()
        expected_value = 'servers'

        message = 'Actual %s, expected %s' % (actual_value, expected_value)
        self.assertEqual(actual_value, expected_value, message)

    def testgetCollectorPathHostNone(self):
        metric = Metric('servers.host.cpu.total.idle',
                        0)

        actual_value = metric.getCollectorPath()
        expected_value = 'cpu'

        message = 'Actual %s, expected %s' % (actual_value, expected_value)
        self.assertEqual(actual_value, expected_value, message)

    def testgetMetricPathHostNone(self):
        metric = Metric('servers.host.cpu.total.idle',
                        0)

        actual_value = metric.getMetricPath()
        expected_value = 'total.idle'

        message = 'Actual %s, expected %s' % (actual_value, expected_value)
        self.assertEqual(actual_value, expected_value, message)

    def test_parse(self):
        metric = Metric('test.parse', 0)

        actual_value = str(metric).strip()
        expected_value = str(Metric.parse(actual_value)).strip()

        message = 'Actual %s, expected %s' % (actual_value, expected_value)
        self.assertEqual(actual_value, expected_value, message)

    def test_issue_723(self):
        metrics = [
            9.97143369909e-05,
            '9.97143369909e-05',
            0.0000997143369909,
            '0.0000997143369909',
        ]

        for precision in xrange(0, 100):
            for m in metrics:
                metric = Metric('test.723', m, timestamp=0)

                actual_value = str(metric).strip()
                expected_value = 'test.723 0 0'

                message = 'Actual %s, expected %s' % (actual_value,
                                                      expected_value)
                self.assertEqual(actual_value, expected_value, message)
