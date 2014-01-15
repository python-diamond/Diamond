#!/usr/bin/python
# coding=utf-8

import datetime
from test import CollectorTestCase
from test import get_collector_config
from test import run_only
from test import unittest
from mock import patch
from mock import Mock

from diamond.collector import Collector
from elb import ElbCollector

class TestElbCollector(CollectorTestCase):

    def assertRaisesAndContains(self, excClass, contains_str, callableObj, *args, **kwargs):
        try:
            callableObj(*args, **kwargs)
        except excClass, e:
            msg = str(e)
            if contains_str in msg:
                return
            else:
                raise AssertionError, "Exception message does not contain '%s': '%s'" % (contains_str, msg)
        else:
            if hasattr(excClass,'__name__'): excName = excClass.__name__
            else: excName = str(excClass)
            raise AssertionError, "%s not raised" % excName

    def test_throws_exception_when_interval_not_multiple_of_60(self):
        config = get_collector_config('ElbCollector', { 'interval': 10 })
        self.assertRaisesAndContains(Exception, 'multiple of', ElbCollector, *[config, None])

    @patch('elb.cloudwatch')
    @patch('boto.ec2.connect_to_region')
    @patch.object(Collector, 'publish')
    def test_collect(self, publish, connect_to_region, cloudwatch):
        config = get_collector_config(
            'ElbCollector',
            { 'interval': 60,
              'regions' :{
                  'us-west-1': {
                      'elb_names' : ['elb1'],
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
        cw_conn.get_metric_statistics = Mock()
        cw_conn.get_metric_statistics.side_effect = [
            [{u'Timestamp': datetime.datetime(2014, 1, 14, 15, 22), u'Average': 4.0, u'Unit': u'Count'}],
            [{u'Timestamp': datetime.datetime(2014, 1, 14, 15, 22), u'Average': 2.0, u'Unit': u'Count'}],
            [{u'Timestamp': datetime.datetime(2014, 1, 14, 15, 22), u'Sum': 3.0, u'Unit': u'Count'}],
            [{u'Timestamp': datetime.datetime(2014, 1, 14, 15, 22), u'Average': 4.0, u'Unit': u'Count'}],
            [{u'Timestamp': datetime.datetime(2014, 1, 14, 15, 22), u'Sum': 4.0, u'Unit': u'Count'}],
            [{u'Timestamp': datetime.datetime(2014, 1, 14, 15, 22), u'Sum': 4.0, u'Unit': u'Count'}],
            [{u'Timestamp': datetime.datetime(2014, 1, 14, 15, 22), u'Sum': 4.0, u'Unit': u'Count'}],
            [{u'Timestamp': datetime.datetime(2014, 1, 14, 15, 22), u'Sum': 4.0, u'Unit': u'Count'}],
            [{u'Timestamp': datetime.datetime(2014, 1, 14, 15, 22), u'Sum': 4.0, u'Unit': u'Count'}],
            [{u'Timestamp': datetime.datetime(2014, 1, 14, 15, 22), u'Sum': 4.0, u'Unit': u'Count'}],
            [{u'Timestamp': datetime.datetime(2014, 1, 14, 15, 22), u'Sum': 4.0, u'Unit': u'Count'}],
            [{u'Timestamp': datetime.datetime(2014, 1, 14, 15, 22), u'Maximum': 4.0, u'Unit': u'Count'}],
            [{u'Timestamp': datetime.datetime(2014, 1, 14, 15, 22), u'Sum': 4.0, u'Unit': u'Count'}],
        ]

        # ('HealthyHostCount', 'Average'),
        # ('UnhealthyHostCount', 'Average'),
        # ('RequestCount', 'Sum'),
        # ('Latency', 'Average'),
        # ('HTTPCode_ELB_4XX', 'Sum'),
        # ('HTTPCode_ELB_5XX', 'Sum'),
        # ('HTTPCode_Backend_2XX', 'Sum'),
        # ('HTTPCode_Backend_3XX', 'Sum'),
        # ('HTTPCode_Backend_4XX', 'Sum'),
        # ('HTTPCode_Backend_5XX', 'Sum'),
        # ('BackendConnectionErrors', 'Sum'),
        # ('SurgeQueueLength', 'Maximum'),
        # ('SpilloverCount', 'Sum')]

        cloudwatch.connect_to_region = Mock()
        cloudwatch.connect_to_region.return_value = cw_conn

        collector = ElbCollector(config, handlers=[])
        collector.collect()

        print publish.call_args_list

        self.assertPublishedMany(
            publish,
            {
                'us-west-1a.elb1.HealthyHostCount'   : 4,
                'us-west-1a.elb1.UnhealthyHostCount' : 2,
                'us-west-1a.elb1.RequestCount' : 3,
            })

if __name__ == "__main__":
    unittest.main()