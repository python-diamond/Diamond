#!/usr/bin/python
################################################################################

from test import *

from diamond.collector import Collector

import nginx

################################################################################

class RequestStub(object):
    def __init__(self, data):
        self.data = data

    def read(self):
        return self.data

    def readlines(self):
        return self.data.split("\n")

class TestNginxCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('nginx.NginxCollector', {})

        self.collector = nginx.NginxCollector(config, None)

    def urlopen_stub(self, *args, **kwargs):
        return RequestStub(self.getFixture('status').getvalue())

    def urlopen_stub_null(self, *args, **kwargs):
        return RequestStub('')

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        nginx.urllib2.urlopen = self.urlopen_stub
        self.collector.collect()
            
        self.assertPublishedMany(publish_mock, {
            'active_connections' : 3, 
            'conn_accepted' : 396396, 
            'conn_handled' : 396396, 
            'req_handled' : 396396, 
            'act_reads' : 2, 
            'act_writes' : 1, 
            'act_waits' : 0, 
        })

    @patch.object(Collector, 'publish')
    def test_should_fail_gracefully(self, publish_mock):
        nginx.urllib2.urlopen = self.urlopen_stub_null
        self.collector.collect()
            
        self.assertPublishedMany(publish_mock, {})

################################################################################
if __name__ == "__main__":
    unittest.main()
