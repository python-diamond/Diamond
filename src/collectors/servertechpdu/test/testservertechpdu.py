#!/usr/bin/python
# coding=utf-8
################################################################################

from test import CollectorTestCase
from test import get_collector_config

from servertechpdu import ServerTechPDUCollector


class TestServerTechPDUCollector(CollectorTestCase):
    def setUp(self, allowed_names=None):
        if not allowed_names:
            allowed_names = []
        config = get_collector_config('ServerTechPDUCollector', {
            'allowed_names': allowed_names,
            'interval': 1
        })
        self.collector = ServerTechPDUCollector(config, None)

    def test_import(self):
        self.assertTrue(ServerTechPDUCollector)
