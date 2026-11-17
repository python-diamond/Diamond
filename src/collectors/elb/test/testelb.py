#!/usr/bin/python3
# coding=utf-8

import datetime

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from test import patch
from test import run_only
from test import Mock

from diamond.collector import Collector
import elb
from elb import ElbCollector


def run_only_if_boto3_is_available(func):
    try:
        import boto3
    except ImportError:
        boto3 = None

    return run_only(func, lambda: boto3 is not None)


def datapoints(ts):
    return [
        {'Datapoints': [{u'Timestamp': ts, stat: value, u'Unit': u'Count'}]}
        for stat, value in [
            (u'Average', 1.0), (u'Average', 2.0), (u'Sum', 3.0),
            (u'Average', 4.0), (u'Sum', 6.0), (u'Sum', 7.0), (u'Sum', 8.0),
            (u'Sum', 9.0), (u'Sum', 10.0), (u'Sum', 11.0), (u'Sum', 12.0),
            (u'Maximum', 13.0), (u'Sum', 14.0)]]


def mock_boto3(boto3, ec2_client, elb_client, cw_client):
    clients = {'ec2': ec2_client, 'elb': elb_client, 'cloudwatch': cw_client}
    boto3.client.side_effect = lambda service, **kwargs: clients[service]


EXPECTED = {
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
}


class TestElbCollector(CollectorTestCase):

    def setUp(self):
        # get_zones is memoized across tests
        elb.get_zones.cache.clear()

    @run_only_if_boto3_is_available
    def test_throws_exception_when_interval_not_multiple_of_60(self):
        config = get_collector_config('ElbCollector',
                                      {'enabled': True,
                                       'interval': 10})
        assertRaisesAndContains(Exception, 'multiple of',
                                ElbCollector, *[config, None])

    @run_only_if_boto3_is_available
    @patch('elb.boto3')
    @patch.object(Collector, 'publish_metric')
    def test_ignore(self, publish_metric, boto3):
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

        ec2_client = Mock()
        ec2_client.describe_availability_zones.return_value = {
            'AvailabilityZones': [{'ZoneName': 'us-west-1a'}]}

        elb_client = Mock()
        elb_client.get_paginator.return_value.paginate.return_value = [
            {'LoadBalancerDescriptions': [{'LoadBalancerName': 'elb1'},
                                          {'LoadBalancerName': 'to_ignore'}]}]

        cw_client = Mock()
        ts = datetime.datetime.utcnow().replace(second=0, microsecond=0)
        cw_client.get_metric_statistics.side_effect = datapoints(ts)

        mock_boto3(boto3, ec2_client, elb_client, cw_client)

        collector = ElbCollector(config, handlers=[])

        target = ts + datetime.timedelta(minutes=1)
        with patch.object(datetime, 'datetime',
                          Mock(wraps=datetime.datetime)) as patched:
            patched.utcnow.return_value = target
            collector.collect()

        self.assertPublishedMetricMany(publish_metric, EXPECTED)
        self.assertEqual(cw_client.get_metric_statistics.call_count, 13)

    @run_only_if_boto3_is_available
    @patch('elb.boto3')
    @patch.object(Collector, 'publish_metric')
    def test_collect(self, publish_metric, boto3):
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

        ec2_client = Mock()
        ec2_client.describe_availability_zones.return_value = {
            'AvailabilityZones': [{'ZoneName': 'us-west-1a'}]}

        cw_client = Mock()
        ts = datetime.datetime.utcnow().replace(second=0, microsecond=0)
        cw_client.get_metric_statistics.side_effect = datapoints(ts)

        mock_boto3(boto3, ec2_client, Mock(), cw_client)

        collector = ElbCollector(config, handlers=[])

        target = ts + datetime.timedelta(minutes=1)
        with patch.object(datetime, 'datetime',
                          Mock(wraps=datetime.datetime)) as patched:
            patched.utcnow.return_value = target
            collector.collect()

        self.assertPublishedMetricMany(publish_metric, EXPECTED)
        cw_client.get_metric_statistics.assert_any_call(
            Namespace='AWS/ELB',
            MetricName='HealthyHostCount',
            Dimensions=[
                {'Name': 'LoadBalancerName', 'Value': 'elb1'},
                {'Name': 'AvailabilityZone', 'Value': 'us-west-1a'}],
            StartTime=ts,
            EndTime=target,
            Period=60,
            Statistics=['Average'])


def assertRaisesAndContains(excClass, contains_str, callableObj, *args,
                            **kwargs):
    try:
        callableObj(*args, **kwargs)
    except excClass as e:
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
