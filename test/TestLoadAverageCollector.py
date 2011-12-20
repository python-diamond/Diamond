#!/usr/bin/python
################################################################################

from common import *

from diamond.collector import Collector
from LoadAverageCollector import LoadAverageCollector

################################################################################

class TestLoadAverageCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('LoadAverageCollector', {
            'interval': 10
        })

        self.collector = LoadAverageCollector(config, None)

    @patch('__builtin__.open')
    @patch.object(Collector, 'publish')
    def test_should_open_proc_loadavg(self, publish_mock, open_mock):
        open_mock.return_value = StringIO('')
        self.collector.collect()
        open_mock.assert_called_once_with('/proc/loadavg')

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        LoadAverageCollector.PROC = get_fixture_path('proc_loadavg')
        self.collector.collect()

        self.assertPublishedMany(publish_mock, {
            '01' : (0.00, 2),
            '05' : (0.32, 2),
            '15' : (0.56, 2),
            'processes_running' : 1,
            'processes_total'   : 235
        })

################################################################################
if __name__ == "__main__":
    unittest.main()
