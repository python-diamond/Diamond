#!/usr/bin/python
# coding=utf-8
###############################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import Mock
from mock import patch

from libvirtkvm import LibvirtKVMCollector

###############################################################################

class TestLibvirtKVMCollector(CollectorTestCase):

    def setUp(self):
        config = get_collector_config('LibvirtKVMCollector', {
        })
        self.collector = LibvirtKVMCollector(config, None)

    def test_import(self):
        self.assertTrue(LibvirtKVMCollector)

    @patch('libvirt')
    @patch.object(Collector, 'publish')

    def test_should_work_with_real_data(self, publish_mock, libvirt_mock):
        libvirt = Mock()
        conn_mock = Mock()
        dom_mock = Mock()

        listDomainsID = [ 1 ]

        libvirt_mock.return_value = libvirt
        libvirt.openReadOnly.return_value = conn_mock
        conn_mock.listDomainsID.return_value = listDomainsID
        conn_mock.lookupByID.return_value = dom_mock

        dom_mock.UUIDString.return_value = "uuid"

        dom_mock.getCPUStats.return_value = [{'cpu_time': 30375130070L,
                                                'system_time': 6980000000L,
                                                'user_time': 3120000000L}]

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
