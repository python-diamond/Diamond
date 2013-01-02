#!/usr/bin/python
# coding=utf-8
################################################################################

from test import CollectorTestCase
from test import get_collector_config

from openstackswift import OpenstackSwiftCollector


class TestOpenstackSwiftCollector(CollectorTestCase):
    def setUp(self, allowed_names=None):
        if not allowed_names:
            allowed_names = []
        config = get_collector_config('OpenstackSwiftCollector', {
            'allowed_names': allowed_names,
            'interval': 1
        })
        self.collector = OpenstackSwiftCollector(config, None)

    def test_import(self):
        self.assertTrue(OpenstackSwiftCollector)
