#!/usr/bin/python
# coding=utf-8
###############################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest

from statsdCollector import StatsdCollector, _clean_key, parse_metrics, NewMetric

###############################################################################


class TestStatsdCollector(CollectorTestCase):

    def setUp(self):
        config = get_collector_config('StatsdCollector', {})
        self.collector = StatsdCollector(config, None)

    def test_import(self):
        self.assertTrue(StatsdCollector)

    def test_clean_key(self):
        self.assertEqual(_clean_key('test/this/key'), 'test-this-key')
        self.assertEqual(_clean_key('test key'), 'test_key')
        self.assertEqual(_clean_key('normal_key'), 'normal_key')
        self.assertEqual(_clean_key('@special-remove@'), 'special-remove')
        self.assertEqual(_clean_key('normal.key'), 'normal.key')

    def test_parse_metrics(self):
        raw_metrics = 'gorets:1|c\nglork:320|ms\ngaugor:333|g'
        expected_values = [NewMetric(path='gorets', value='1', metric_type='COUNTER'),
                           NewMetric(path='glork', value='320', metric_type='GAUGE'),
                           NewMetric(path='gaugor', value='333', metric_type='GAUGE'),]
        parsed_metrics = parse_metrics(raw_metrics)
        for metric, expected_value in zip(parsed_metrics, expected_values) :
            self.assertEqual(metric.path, expected_value.path)
            self.assertEqual(metric.value, expected_value.value)
            self.assertEqual(metric.metric_type, expected_value.metric_type)

        with self.assertRaises(ValueError):
            next(parse_metrics('nuniques:765|s'))

###############################################################################
if __name__ == "__main__":
    unittest.main()

