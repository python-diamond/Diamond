#!/usr/bin/python
# coding=utf-8
################################################################################

from test import CollectorTestCase
from test import get_collector_config

from lmsensors import LMSensorsCollector


class TestLMSensorsCollector(CollectorTestCase):
    def setUp(self, allowed_names=None):
        if not allowed_names:
            allowed_names = []
        config = get_collector_config('LMSensorsCollector', {
            'allowed_names': allowed_names,
            'interval': 1
        })
        self.collector = LMSensorsCollector(config, None)

    def test_import(self):
        self.assertTrue(LMSensorsCollector)
