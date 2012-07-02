#!/usr/bin/python
################################################################################

from test import *

from diamond.collector import Collector
from resqueweb import ResqueWebCollector

import resqueweb
import urllib2

################################################################################

class RequestStub(object):
    def __init__(self, data):
        self.data = data

    def read(self):
        return self.data

class TestResqueWebCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('resqueweb.ResqueWebCollector', {
            'interval': 10
        })

        self.collector = ResqueWebCollector(config, None)

    def urlopen_stub(self, *args, **kwargs):
        return RequestStub(self.getFixture('stats.txt').getvalue())

    def urlopen_stub_null(self, *args, **kwargs):
        return RequestStub('')

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        resqueweb.urllib2.urlopen = self.urlopen_stub
        self.collector.collect()
            
        self.assertPublishedMany(publish_mock, {
            'pending.current' : 2, 
            'processed.total' : 11686516, 
            'failed.total' : 38667, 
            'workers.current' : 9, 
            'working.current' : 2, 
            'queue.low.current' : 4, 
            'queue.mail.current' : 3, 
            'queue.realtime.current' : 9, 
            'queue.normal.current' : 1,
        })

    @patch.object(Collector, 'publish')
    def test_should_fail_gracefully(self, publish_mock):
        resqueweb.urllib2.urlopen = self.urlopen_stub_null
        self.collector.collect()
            
        self.assertPublishedMany(publish_mock, {})

################################################################################
if __name__ == "__main__":
    unittest.main()
