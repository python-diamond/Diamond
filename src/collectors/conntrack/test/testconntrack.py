#!/usr/bin/python
################################################################################

from test import *

from diamond.collector import Collector
from conntrack import ConnTrackCollector

################################################################################

class TestConnTrackCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('ConnTrackCollector', {
            'interval': 10
        })

        self.collector = ConnTrackCollector(config, None)
        self.collector.COMMAND[0] = 'true'

    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_work_with_synthetic_data(self, publish_mock):
        with patch('subprocess.Popen.communicate', Mock(return_value =
            ( 'net.netfilter.nf_conntrack_count = 33' , '')
        )):
            self.collector.collect()

        self.assertPublishedMany(publish_mock, {
            'nf_conntrack_count' : 33.0
        })

################################################################################
if __name__ == "__main__":
    unittest.main()
