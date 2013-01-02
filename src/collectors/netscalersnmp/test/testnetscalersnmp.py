#!/usr/bin/python
# coding=utf-8
################################################################################

from test import CollectorTestCase
from test import get_collector_config

from netscalersnmp import NetscalerSNMPCollector


class TestNetscalerSNMPCollector(CollectorTestCase):
    def setUp(self, allowed_names=None):
        if not allowed_names:
            allowed_names = []
        config = get_collector_config('NetscalerSNMPCollector', {
            'allowed_names': allowed_names,
            'interval': 1
        })
        self.collector = NetscalerSNMPCollector(config, None)

    def test_import(self):
        self.assertTrue(NetscalerSNMPCollector)
