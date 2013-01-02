#!/usr/bin/python
# coding=utf-8
################################################################################

from test import CollectorTestCase
from test import get_collector_config

from snmp import SNMPCollector


class TestSNMPCollector(CollectorTestCase):
    def setUp(self, allowed_names=None):
        if not allowed_names:
            allowed_names = []
        config = get_collector_config('SNMPCollector', {
            'allowed_names': allowed_names,
            'interval': 1
        })
        self.collector = SNMPCollector(config, None)

    def test_import(self):
        self.assertTrue(SNMPCollector)
