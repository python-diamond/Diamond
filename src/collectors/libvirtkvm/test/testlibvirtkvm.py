#!/usr/bin/python
# coding=utf-8
###############################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest

from libvirtkvm import LibvirtKVMCollector


###############################################################################

class TestLibvirtKVMCollector(CollectorTestCase):

    def setUp(self):
        config = get_collector_config('LibvirtKVMCollector', {
        })
        self.collector = LibvirtKVMCollector(config, None)

    def test_import(self):
        self.assertTrue(LibvirtKVMCollector)

    @patch.object(Collector, 'publish')

    def test_should_work_with_real_data(self, publish_mock, conn_mock):
        LibvirtKVMCollector.conn = Mock()
        conn = True
        listDomainsID = [ 1 ]
        lookupByID = True

        LibvirtKVMCollector.conn_mock = Mock()

        dom.getCPUStats
        dom.getCPUStats

        LibvirtKVMCollector.dom. = self.getFixturePath('proc_meminfo')
        self.collector.collect()

        metrics = {
            'MemTotal': 49554212,
            'MemFree': 35194496,
            'Buffers': 1526304,
            'Cached': 10726736,
            'Active': 10022168,
            'Dirty': 24748,
            'Inactive': 2524928,
            'Shmem': 276,
            'SwapTotal': 262143996,
            'SwapFree': 262143996,
            'SwapCached': 0,
            'VmallocTotal': 34359738367,
            'VmallocUsed': 445452,
            'VmallocChunk': 34311049240
        }


###############################################################################
if __name__ == "__main__":
    unittest.main()
