#!/usr/bin/python
################################################################################

from test import *

from diamond.collector import Collector

import elasticsearch

################################################################################

class RequestStub(object):
    def __init__(self, data):
        self.data = data

    def read(self):
        return self.data

    def readlines(self):
        return self.data.split("\n")

class TestElasticSearchCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('elasticsearch.ElasticSearchCollector', {})

        self.collector = elasticsearch.ElasticSearchCollector(config, None)

    def urlopen_stub(self, *args, **kwargs):
        return RequestStub(self.getFixture('stats').getvalue())

    def urlopen_stub_null(self, *args, **kwargs):
        return RequestStub('')

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        elasticsearch.urllib2.urlopen = self.urlopen_stub
        self.collector.collect()
            
        self.assertPublishedMany(publish_mock, {
            'http.current' : 1, 
            
            'indices.docs.count' : 11968062, 
            'indices.docs.deleted' : 2692068, 
            'indices.datastore.size': 22724243633,

            'process.cpu.percent' : 58, 
            
            'process.mem.resident' : 5192126464, 
            'process.mem.share' : 11075584, 
            'process.mem.virtual' : 7109668864, 

            'disk.reads.count': 55996, 
            'disk.reads.size': 1235387392,
            'disk.writes.count': 5808198,
            'disk.writes.size': 23287275520,

            
        })

    # @patch.object(Collector, 'publish')
    # def test_should_fail_gracefully(self, publish_mock):
    #     elasticsearch.urllib2.urlopen = self.urlopen_stub_null
    #     self.collector.collect()
            
    #     self.assertPublishedMany(publish_mock, {})

################################################################################
if __name__ == "__main__":
    unittest.main()
