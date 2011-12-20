#!/usr/bin/python
################################################################################

from common import *

from diamond.collector import Collector
from VMStatCollector import VMStatCollector

################################################################################

class TestVMStatCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('VMStatCollector', {
            'interval': 10
        })

        self.collector = VMStatCollector(config, None)

    @patch('__builtin__.open')
    @patch.object(Collector, 'publish')
    def test_should_open_proc_vmstat(self, publish_mock, open_mock):
        open_mock.return_value = StringIO('')
        self.collector.collect()
        open_mock.assert_called_once_with('/proc/vmstat')

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        VMStatCollector.PROC = get_fixture_path('proc_vmstat_1')
        self.collector.collect()

        self.assertPublishedMany(publish_mock, {})

        VMStatCollector.PROC = get_fixture_path('proc_vmstat_2')
        self.collector.collect()

        self.assertPublishedMany(publish_mock, {
            'pgpgin'  : 0.0,
            'pgpgout' : 9.2,
            'pswpin'  : 0.0,
            'pswpout' : 0.0,
        })


################################################################################
if __name__ == "__main__":
    unittest.main()
