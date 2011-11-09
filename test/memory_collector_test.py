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
    def test_should_open_proc_fs(self, publish_mock, open_mock):
        open_mock.return_value.__iter__.return_value = iter([])
        self.collector.collect()
        open_mock.assert_called_once_with('/proc/meminfo', 'r')

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        MemoryCollector.PROC = get_fixture_path('proc_meminfo')
        self.collector.collect()

        self.assertPublishedMany(publish_mock, {
            'total' : '49554212',
            'free' : '35194496',
            'buffers' : '1526304',
            'cached' : '10726736',
            'active' : '10022168',
            'inactive' : '2524928',
            'swap.total' : '262143996',
            'swap.free' : '262143996',
            'swap.cached' : '0',
            'vm.total' : '34359738367',
            'vm.used' : '445452',
        })
        publish_mock.reset_mock()        

################################################################################
if __name__ == "__main__":
    unittest.main()
