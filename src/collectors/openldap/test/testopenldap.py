#!/usr/bin/python
# coding=utf-8
##########################################################################

from test import CollectorTestCase
from test import get_collector_config

from openldap import OpenLDAPCollector


class TestOpenLDAPCollector(CollectorTestCase):

    def setUp(self, allowed_names=None):
        if not allowed_names:
            allowed_names = []
        config = get_collector_config('OpenLDAPCollector', {
        })
        self.collector = OpenLDAPCollector(config, None)

    def test_import(self):
        self.assertTrue(OpenLDAPCollector)
