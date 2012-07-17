#!/usr/bin/python
################################################################################

from test import *

from diamond.collector import Collector
from userscripts import UserScriptsCollector

################################################################################

class TestUserScriptsCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('UserScriptsCollector', {
            'interval': 10,
            'scripts_path': os.path.dirname(__file__)+'/fixtures/',
        })

        self.collector = UserScriptsCollector(config, None)

    @patch.object(Collector, 'publish')
    def test_should_work_with_example(self, publish_mock):
        self.collector.collect()

        self.assertPublishedMany(publish_mock, {
            'example.1': 42, 
            'example.2': 24,
        })

################################################################################
if __name__ == "__main__":
    unittest.main()
