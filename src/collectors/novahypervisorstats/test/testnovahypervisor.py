#!/usr/bin/env python
# coding=utf-8
##########################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest

from novahypervisorstats import NovaHypervisorStatsCollector

##########################################################################


class TestNovaHypervisorStatsCollector(CollectorTestCase):

    def setUp(self):
        config = get_collector_config('NovaHypervisorStatsCollector', {
            'interval': 10
        })

        self.collector = NovaHypervisorStatsCollector(config, None)

    def test_import(self):
        self.assertTrue(NovaHypervisorStatsCollector)

##########################################################################
if __name__ == "__main__":
    unittest.main()
