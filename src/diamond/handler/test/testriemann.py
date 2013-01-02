#!/usr/bin/python
# coding=utf-8
################################################################################

from test import unittest
import configobj

from diamond.handler.riemann import RiemannHandler
from diamond.metric import Metric


class TestRiemannHandler(unittest.TestCase):
    def test_metric_to_riemann_event(self):
        config = configobj.ConfigObj()
        config['host'] = 'localhost'
        config['port'] = 5555

        handler = RiemannHandler(config)
        metric = Metric('servers.com.example.www.cpu.total.idle',
                        0,
                        timestamp=1234567,
                        host='com.example.www')

        event = handler._metric_to_riemann_event(metric)

        self.assertEqual(event, {
            'host': 'com.example.www',
            'service': 'servers.cpu.total.idle',
            'time': 1234567,
            'metric': 0.0,
        })
