#!/usr/bin/python
# coding=utf-8
################################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import Mock
from mock import patch

from diamond.collector import Collector

from unbound import UnboundCollector

################################################################################


class TestUnboundCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('UnboundCollector', {})

        self.collector = UnboundCollector(config, None)

    def test_import(self):
        self.assertTrue(UnboundCollector)

    @patch.object(Collector, 'publish')
    def test_should_work_wtih_real_data(self, publish_mock):
        fixture_data = self.getFixture('unbound_stats').getvalue()
        collector_mock = patch.object(UnboundCollector,
                                      'get_unbound_control_output',
                                      Mock(return_value=fixture_data))
        collector_mock.start()
        self.collector.collect()
        collector_mock.stop()

        metrics = {
            'thread0.num.queries': 10028,
            'thread0.num.cachehits': 10021,
            'thread0.num.cachemiss': 7,
            'thread0.num.prefetch': 1,
            'thread0.num.recursivereplies': 9,
            'thread0.requestlist.avg': 1.25,
            'thread0.requestlist.max': 2,
            'thread0.requestlist.overwritten': 0,
            'thread0.requestlist.exceeded': 0,
            'thread0.requestlist.current.all': 1,
            'thread0.requestlist.current.user': 1,
            'thread0.recursion.time.avg': 9.914812,
            'thread0.recursion.time.median': 0.08192,
            'total.num.queries': 125609,
            'total.num.cachehits': 125483,
            'total.num.cachemiss': 126,
            'total.num.prefetch': 16,
            'total.num.recursivereplies': 136,
            'total.requestlist.avg': 5.07746,
            'total.requestlist.max': 10,
            'total.requestlist.overwritten': 0,
            'total.requestlist.exceeded': 0,
            'total.requestlist.current.all': 23,
            'total.requestlist.current.user': 23,
            'total.recursion.time.avg': 13.045485,
            'total.recursion.time.median': 0.06016,
            'time.now': 1361926066.384873,
            'time.up': 3006293.632453,
            'time.elapsed': 9.981882,
            'mem.total.sbrk': 26767360,
            'mem.cache.rrset': 142606276,
            'mem.cache.message': 71303005,
            'mem.mod.iterator': 16532,
            'mem.mod.validator': 1114579,
            'num.query.type.A': 25596,
            'num.query.type.PTR': 39,
            'num.query.type.MX': 91,
            'num.query.type.AAAA': 99883,
            'num.query.class.IN': 125609,
            'num.query.opcode.QUERY': 125609,
            'num.query.tcp': 0,
            'num.query.ipv6': 0,
            'num.query.flags.QR': 0,
            'num.query.flags.AA': 0,
            'num.query.flags.TC': 0,
            'num.query.flags.RD': 125609,
            'num.query.flags.RA': 0,
            'num.query.flags.Z': 0,
            'num.query.flags.AD': 0,
            'num.query.flags.CD': 62,
            'num.query.edns.present': 62,
            'num.query.edns.DO': 62,
            'num.answer.rcode.NOERROR': 46989,
            'num.answer.rcode.SERVFAIL': 55,
            'num.answer.rcode.NXDOMAIN': 78575,
            'num.answer.rcode.nodata': 20566,
            'num.answer.secure': 0,
            'num.answer.bogus': 0,
            'num.rrset.bogus': 0,
            'unwanted.queries': 0,
            'unwanted.replies': 0,
            'histogram.16s+': 0.0,
            'histogram.256ms+': 3.0,
            'histogram.4s+': 1.0,
            'histogram.2s+': 0.0,
            'histogram.1s+': 0.0,
            'histogram.2ms+': 0.0,
            'histogram.1ms': 39.0,
            'histogram.32ms+': 18.0,
            'histogram.4ms+': 0.0,
            'histogram.16ms+': 10.0,
            'histogram.1ms+': 5.0,
            'histogram.32s+': 3.0,
            'histogram.512ms+': 6.0,
            'histogram.128ms+': 19.0,
            'histogram.64ms+': 20.0,
            'histogram.8ms+': 3.0,
            'histogram.64s+': 9.0,
            'histogram.8s+': 0.0,
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

    @patch.object(Collector, 'publish')
    def test_should_fail_gracefully(self, publish_mock):
        collector_mock = patch.object(UnboundCollector,
                                      'get_unbound_control_output',
                                      Mock(return_value=''))
        collector_mock.start()
        self.collector.collect()
        collector_mock.stop()

        self.assertPublishedMany(publish_mock, {})

    @patch.object(Collector, 'publish')
    def test_exclude_histogram(self, publish_mock):
        self.collector.config['histogram'] = False

        fixture_data = self.getFixture('unbound_stats').getvalue()
        collector_mock = patch.object(UnboundCollector,
                                      'get_unbound_control_output',
                                      Mock(return_value=fixture_data))
        collector_mock.start()
        self.collector.collect()
        collector_mock.stop()

        metrics = {
            'thread0.num.queries': 10028,
            'thread0.num.cachehits': 10021,
            'thread0.num.cachemiss': 7,
            'thread0.num.prefetch': 1,
            'thread0.num.recursivereplies': 9,
            'thread0.requestlist.avg': 1.25,
            'thread0.requestlist.max': 2,
            'thread0.requestlist.overwritten': 0,
            'thread0.requestlist.exceeded': 0,
            'thread0.requestlist.current.all': 1,
            'thread0.requestlist.current.user': 1,
            'thread0.recursion.time.avg': 9.914812,
            'thread0.recursion.time.median': 0.08192,
            'total.num.queries': 125609,
            'total.num.cachehits': 125483,
            'total.num.cachemiss': 126,
            'total.num.prefetch': 16,
            'total.num.recursivereplies': 136,
            'total.requestlist.avg': 5.07746,
            'total.requestlist.max': 10,
            'total.requestlist.overwritten': 0,
            'total.requestlist.exceeded': 0,
            'total.requestlist.current.all': 23,
            'total.requestlist.current.user': 23,
            'total.recursion.time.avg': 13.045485,
            'total.recursion.time.median': 0.06016,
            'time.now': 1361926066.384873,
            'time.up': 3006293.632453,
            'time.elapsed': 9.981882,
            'mem.total.sbrk': 26767360,
            'mem.cache.rrset': 142606276,
            'mem.cache.message': 71303005,
            'mem.mod.iterator': 16532,
            'mem.mod.validator': 1114579,
            'num.query.type.A': 25596,
            'num.query.type.PTR': 39,
            'num.query.type.MX': 91,
            'num.query.type.AAAA': 99883,
            'num.query.class.IN': 125609,
            'num.query.opcode.QUERY': 125609,
            'num.query.tcp': 0,
            'num.query.ipv6': 0,
            'num.query.flags.QR': 0,
            'num.query.flags.AA': 0,
            'num.query.flags.TC': 0,
            'num.query.flags.RD': 125609,
            'num.query.flags.RA': 0,
            'num.query.flags.Z': 0,
            'num.query.flags.AD': 0,
            'num.query.flags.CD': 62,
            'num.query.edns.present': 62,
            'num.query.edns.DO': 62,
            'num.answer.rcode.NOERROR': 46989,
            'num.answer.rcode.SERVFAIL': 55,
            'num.answer.rcode.NXDOMAIN': 78575,
            'num.answer.rcode.nodata': 20566,
            'num.answer.secure': 0,
            'num.answer.bogus': 0,
            'num.rrset.bogus': 0,
            'unwanted.queries': 0,
            'unwanted.replies': 0,
        }

        histogram = {
            'histogram.16s+': 0.0,
            'histogram.256ms+': 3.0,
            'histogram.4s+': 1.0,
            'histogram.2s+': 0.0,
            'histogram.1s+': 0.0,
            'histogram.2ms+': 0.0,
            'histogram.1ms': 39.0,
            'histogram.32ms+': 18.0,
            'histogram.4ms+': 0.0,
            'histogram.16ms+': 10.0,
            'histogram.1ms+': 5.0,
            'histogram.32s+': 3.0,
            'histogram.512ms+': 6.0,
            'histogram.128ms+': 19.0,
            'histogram.64ms+': 20.0,
            'histogram.8ms+': 3.0,
            'histogram.64s+': 9.0,
            'histogram.8s+': 0.0,
        }

        self.assertPublishedMany(publish_mock, metrics)
        self.assertUnpublishedMany(publish_mock, histogram)

################################################################################
if __name__ == "__main__":
    unittest.main()
