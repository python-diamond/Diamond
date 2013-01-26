#!/usr/bin/python
# coding=utf-8
###############################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from test import run_only
from mock import Mock
from mock import patch

from diamond.collector import Collector
from xen_collector import XENCollector


###############################################################################


def run_only_if_libvirt_is_available(func):
    try:
        import libvirt
        libvirt  # workaround for pyflakes issue #13
    except ImportError:
        libvirt = None
    pred = lambda: libvirt is not None
    return run_only(func, pred)


class TestXENCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('XENCollector', {
        })
        self.collector = XENCollector(config, None)

    def test_import(self):
        self.assertTrue(XENCollector)

    @run_only_if_libvirt_is_available
    @patch('os.statvfs')
    @patch('libvirt.openReadOnly')
    @patch.object(Collector, 'publish')
    def test_centos6(self, publish_mock, libvirt_mock, os_mock):

        class info:
            def __init__(self, id):
                self.id = id

            def info(self):
                if self.id == 0:
                    return [1, 49420888L, 49420888L, 8, 911232000000000L]
                if self.id == 1:
                    return [1, 2097152L,  2097152L,  2, 310676150000000L]
                if self.id == 2:
                    return [1, 2097152L,  2097152L,  2, 100375300000000L]
                if self.id == 3:
                    return [1, 10485760L, 10485760L, 2, 335312040000000L]
                if self.id == 4:
                    return [1, 10485760L, 10485760L, 2, 351313480000000L]

        libvirt_m = Mock()
        libvirt_m.getInfo.return_value = ['x86_64', 48262, 8, 1200, 2, 1, 4, 1]
        libvirt_m.listDomainsID.return_value = [0, 2, 1, 4, 3]

        def lookupByIdMock(id):
            lookup = info(id)
            return lookup

        libvirt_m.lookupByID = lookupByIdMock

        libvirt_mock.return_value = libvirt_m

        statsvfs_mock = Mock()
        statsvfs_mock.f_bavail = 74492145
        statsvfs_mock.f_frsize = 4096

        os_mock.return_value = statsvfs_mock

        self.collector.collect()

        metrics = {
            'TotalCores': 8.000000,
            'InstalledMem': 48262.000000,
            'MemAllocated': 24576.000000,
            'MemFree': 23686.000000,
            'DiskFree': 297968580.000000,
            'FreeCores': 0.000000,
            'AllocatedCores': 8.000000,
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)


###############################################################################
if __name__ == "__main__":
    unittest.main()
