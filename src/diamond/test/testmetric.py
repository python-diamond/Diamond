#!/usr/bin/python
# coding=utf-8
################################################################################

from __future__ import with_statement

from test import CollectorTestCase
from test import unittest
from mock import Mock
from mock import patch

from diamond.metric import Metric

class TestMetric(CollectorTestCase):
    
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
