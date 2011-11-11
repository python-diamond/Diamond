#!/usr/bin/python
################################################################################

from common import *

from diamond.collector import Collector
from memory_collector import MemoryCollector

################################################################################

class TestMemoryCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('MemoryCollector', {
            'interval': 10
        })

        self.collector = MemoryCollector(config, None)

    @patch('__builtin__.open')
    @patch.object(Collector, 'publish')
    def test_should_open_proc_meminfo(self, publish_mock, open_mock):
        open_mock.return_value = StringIO('')
        self.collector.collect()
        open_mock.assert_called_once_with('/proc/meminfo')

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        MemoryCollector.PROC = get_fixture_path('proc_meminfo')
        self.collector.collect()

        self.assertPublishedMany(publish_mock, {
            'total'       : '49554212',
            'free'        : '35194496',
            'buffers'     : '1526304',
            'cached'      : '10726736',
            'active'      : '10022168',
            'inactive'    : '2524928',
            'swap_total'  : '262143996',
            'swap_free'   : '262143996',
            'swap_cached' : '0',
            'vm_total'    : '34359738367',
            'vm_used'     : '445452',
            'vm_chunk'    : '34311049240'
        })

################################################################################
if __name__ == "__main__":
    unittest.main()
