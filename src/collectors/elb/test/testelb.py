#!/usr/bin/python
# coding=utf-8

import datetime
import mock

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import patch
from test import run_only
from mock import Mock

from diamond.collector import Collector
from elb import ElbCollector


def run_only_if_boto_is_available(func):
    try:
        import boto
    except ImportError:
        boto = None
    pred = lambda: boto is not None
    return run_only(func, pred)


class TestElbCollector(CollectorTestCase):

    @run_only_if_boto_is_available
    def test_throws_exception_when_interval_not_multiple_of_60(self):
        config = get_collector_config('ElbCollector',
                                      {'enabled': True,
                                       'interval': 10})
        assertRaisesAndContains(Exception, 'multiple of',
                                ElbCollector, *[config, None])

    @run_only_if_boto_is_available
    @patch('elb.cloudwatch')
    @patch('boto.ec2.connect_to_region')
    @patch('boto.ec2.elb.connect_to_region')
    @patch.object(Collector, 'publish_metric')
    def test_ignore(self, publish_metric, elb_connect_to_region,
                    ec2_connect_to_region, cloudwatch):
        config = get_collector_config(
            'ElbCollector',
            {
                'enabled': True,
                'interval': 60,
                'regions': {
                    'us-west-1': {}
                },
                'elbs_ignored': ['^to_ignore', ],
            })

        az = Mock()
        az.name = 'us-west-1a'

        ec2_conn = Mock()
        ec2_conn.get_all_zones = Mock()
        ec2_conn.get_all_zones.return_value = [az]
        ec2_connect_to_region.return_value = ec2_conn

        elb1 = Mock()
        elb1.name = 'elb1'

        elb2 = Mock()
        elb2.name = 'to_ignore'

        elb_conn = Mock()
        elb_conn.get_all_load_balancers = Mock()
        elb_conn.get_all_load_balancers.return_value = [elb1, elb2]
        elb_connect_to_region.return_value = elb_conn

        cw_conn = Mock()
        cw_conn.region = Mock()
        cw_conn.region.name = 'us-west-1'
        cw_conn.get_metric_statistics = Mock()
        ts = datetime.datetime.utcnow().replace(second=0, microsecond=0)

        cw_conn.get_metric_statistics.side_effect = [
            [{u'Timestamp': ts, u'Average': 1.0, u'Unit': u'Count'}],
            [{u'Timestamp': ts, u'Average': 2.0, u'Unit': u'Count'}],
            [{u'Timestamp': ts, u'Sum': 3.0, u'Unit': u'Count'}],
            [{u'Timestamp': ts, u'Average': 4.0, u'Unit': u'Count'}],
            [{u'Timestamp': ts, u'Sum': 6.0, u'Unit': u'Count'}],
            [{u'Timestamp': ts, u'Sum': 7.0, u'Unit': u'Count'}],
            [{u'Timestamp': ts, u'Sum': 8.0, u'Unit': u'Count'}],
            [{u'Timestamp': ts, u'Sum': 9.0, u'Unit': u'Count'}],
            [{u'Timestamp': ts, u'Sum': 10.0, u'Unit': u'Count'}],
            [{u'Timestamp': ts, u'Sum': 11.0, u'Unit': u'Count'}],
            [{u'Timestamp': ts, u'Sum': 12.0, u'Unit': u'Count'}],
            [{u'Timestamp': ts, u'Maximum': 13.0, u'Unit': u'Count'}],
            [{u'Timestamp': ts, u'Sum': 14.0, u'Unit': u'Count'}],
        ]

        cloudwatch.connect_to_region = Mock()
        cloudwatch.connect_to_region.return_value = cw_conn

        collector = ElbCollector(config, handlers=[])

        target = ts + datetime.timedelta(minutes=1)
        with mock.patch.object(datetime, 'datetime',
                               mock.Mock(wraps=datetime.datetime)) as patched:
            patched.utcnow.return_value = target
            collector.collect()

        self.assertPublishedMetricMany(
            publish_metric,
            {
                'us-west-1a.elb1.HealthyHostCount': 1,
                'us-west-1a.elb1.UnHealthyHostCount': 2,
                'us-west-1a.elb1.RequestCount': 3,
                'us-west-1a.elb1.Latency': 4,
                'us-west-1a.elb1.HTTPCode_ELB_4XX': 6,
                'us-west-1a.elb1.HTTPCode_ELB_5XX': 7,
                'us-west-1a.elb1.HTTPCode_Backend_2XX': 8,
                'us-west-1a.elb1.HTTPCode_Backend_3XX': 9,
                'us-west-1a.elb1.HTTPCode_Backend_4XX': 10,
                'us-west-1a.elb1.HTTPCode_Backend_5XX': 11,
                'us-west-1a.elb1.BackendConnectionErrors': 12,
                'us-west-1a.elb1.SurgeQueueLength': 13,
                'us-west-1a.elb1.SpilloverCount': 14,
            })

    @run_only_if_boto_is_available
    @patch('elb.cloudwatch')
    @patch('boto.ec2.connect_to_region')
    @patch.object(Collector, 'publish_metric')
    def test_collect(self, publish_metric, connect_to_region, cloudwatch):
        config = get_collector_config(
            'ElbCollector',
            {
                'enabled': True,
                'interval': 60,
                'regions': {
                    'us-west-1': {
                        'elb_names': ['elb1'],
                    }
                }
            })

        az = Mock()
        az.name = 'us-west-1a'

        ec2_conn = Mock()
        ec2_conn.get_all_zones = Mock()
        ec2_conn.get_all_zones.return_value = [az]
        connect_to_region.return_value = ec2_conn

        cw_conn = Mock()
        cw_conn.region = Mock()
        cw_conn.region.name = 'us-west-1'
        cw_conn.get_metric_statistics = Mock()
        ts = datetime.datetime.utcnow().replace(second=0, microsecond=0)

        cw_conn.get_metric_statistics.side_effect = [
            [{u'Timestamp': ts, u'Average': 1.0, u'Unit': u'Count'}],
            [{u'Timestamp': ts, u'Average': 2.0, u'Unit': u'Count'}],
            [{u'Timestamp': ts, u'Sum': 3.0, u'Unit': u'Count'}],
            [{u'Timestamp': ts, u'Average': 4.0, u'Unit': u'Count'}],
            [{u'Timestamp': ts, u'Sum': 6.0, u'Unit': u'Count'}],
            [{u'Timestamp': ts, u'Sum': 7.0, u'Unit': u'Count'}],
            [{u'Timestamp': ts, u'Sum': 8.0, u'Unit': u'Count'}],
            [{u'Timestamp': ts, u'Sum': 9.0, u'Unit': u'Count'}],
            [{u'Timestamp': ts, u'Sum': 10.0, u'Unit': u'Count'}],
            [{u'Timestamp': ts, u'Sum': 11.0, u'Unit': u'Count'}],
            [{u'Timestamp': ts, u'Sum': 12.0, u'Unit': u'Count'}],
            [{u'Timestamp': ts, u'Maximum': 13.0, u'Unit': u'Count'}],
            [{u'Timestamp': ts, u'Sum': 14.0, u'Unit': u'Count'}],
        ]

        cloudwatch.connect_to_region = Mock()
        cloudwatch.connect_to_region.return_value = cw_conn

        collector = ElbCollector(config, handlers=[])

        target = ts + datetime.timedelta(minutes=1)
        with mock.patch.object(datetime, 'datetime',
                               mock.Mock(wraps=datetime.datetime)) as patched:
            patched.utcnow.return_value = target
            collector.collect()

        self.assertPublishedMetricMany(
            publish_metric,
            {
                'us-west-1a.elb1.HealthyHostCount': 1,
                'us-west-1a.elb1.UnHealthyHostCount': 2,
                'us-west-1a.elb1.RequestCount': 3,
                'us-west-1a.elb1.Latency': 4,
                'us-west-1a.elb1.HTTPCode_ELB_4XX': 6,
                'us-west-1a.elb1.HTTPCode_ELB_5XX': 7,
                'us-west-1a.elb1.HTTPCode_Backend_2XX': 8,
                'us-west-1a.elb1.HTTPCode_Backend_3XX': 9,
                'us-west-1a.elb1.HTTPCode_Backend_4XX': 10,
                'us-west-1a.elb1.HTTPCode_Backend_5XX': 11,
                'us-west-1a.elb1.BackendConnectionErrors': 12,
                'us-west-1a.elb1.SurgeQueueLength': 13,
                'us-west-1a.elb1.SpilloverCount': 14,
            })


def assertRaisesAndContains(excClass, contains_str, callableObj, *args,
                            **kwargs):
    try:
        callableObj(*args, **kwargs)
    except excClass, e:
        msg = str(e)
        if contains_str in msg:
            return
        else:
            raise AssertionError(
                "Exception message does not contain '%s': '%s'" % (
                    contains_str, msg))
    else:
        if hasattr(excClass, '__name__'):
            excName = excClass.__name__
        else:
            excName = str(excClass)
        raise AssertionError("%s not raised" % excName)

if __name__ == "__main__":
    unittest.main()
