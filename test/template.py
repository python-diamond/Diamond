#!/usr/bin/python
################################################################################

from common import *

################################################################################

class TestXXX(unittest.TestCase):
    def setUp(self):
        self.collector = XXX(get_collector_config(), None)
        pass

    @patch('__builtin__.open')
    @patch.object(diamond.collector.Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        pass

################################################################################
if __name__ == "__main__":
    unittest.main()
