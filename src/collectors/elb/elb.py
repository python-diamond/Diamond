# coding=utf-8

"""
The ELB collector collects metrics for one or more Amazon AWS ELBs

#### Configuration

Below is an example configuration for the ELBCollector.
You can specify an arbitrary amount of regions

```
    enabled = true
    interval = 60

    # Optional
    access_key_id = ...
    secret_access_key = ...

    # Optional - Available keys: region, zone, elb_name, metric_name
    format = $elb_name.$zone.$metric_name

    # Optional - list of regular expressions used to ignore ELBs
    elbs_ignored = ^elb-a$, .*-test$, $test-.*

    [regions]

    [[us-west-1]]
    # Optional - queries all elbs if omitted
    elb_names = elb1, elb2, ...

    [[us-west-2]]
    ...

```

#### Dependencies

 * boto

"""
import calendar
import cPickle
import datetime
import functools
import re
import time
from collections import namedtuple
from string import Template

import diamond.collector
from diamond.metric import Metric

try:
    import boto.ec2.elb
    from boto.ec2 import cloudwatch
except ImportError:
    cloudwatch = False


class memoized(object):
    """Decorator that caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned, and
    the function is not re-evaluated.

    Based upon from http://wiki.python.org/moin/PythonDecoratorLibrary#Memoize
    Nota bene: this decorator memoizes /all/ calls to the function.  For
    a memoization decorator with limited cache size, consider:
    bit.ly/1wtHmlM
    """
    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args, **kwargs):
        # If the function args cannot be used as a cache hash key, fail fast
        key = cPickle.dumps((args, kwargs))
        try:
            return self.cache[key]
        except KeyError:
            value = self.func(*args, **kwargs)
            self.cache[key] = value
            return value

    def __repr__(self):
        """Return the function's docstring."""
        return self.func.__doc__

    def __get__(self, obj, objtype):
        """Support instance methods."""
        return functools.partial(self.__call__, obj)


def utc_to_local(utc_dt):
    """
    :param utc_dt: datetime in UTC
    :return: datetime in the local timezone
    """
    # get integer timestamp to avoid precision lost
    timestamp = calendar.timegm(utc_dt.timetuple())
    local_dt = datetime.datetime.fromtimestamp(timestamp)
    assert utc_dt.resolution >= datetime.timedelta(microseconds=1)
    return local_dt.replace(microsecond=utc_dt.microsecond)


@memoized
def get_zones(region, auth_kwargs):
    """
    :param region: region to get the availability zones for
    :return: list of availability zones
    """
    ec2_conn = boto.ec2.connect_to_region(region, **auth_kwargs)
    return [zone.name for zone in ec2_conn.get_all_zones()]


class ElbCollector(diamond.collector.Collector):

    # default_to_zero means if cloudwatch does not return a stat for the
    # given metric, then just default it to zero.
    MetricInfo = namedtuple(
        'MetricInfo',
        'name aws_type diamond_type precision default_to_zero')

    # AWS metrics for ELBs
    metrics = [
        MetricInfo('HealthyHostCount', 'Average', 'GAUGE', 0, False),
        MetricInfo('UnHealthyHostCount', 'Average', 'GAUGE', 0, False),
        MetricInfo('RequestCount', 'Sum', 'COUNTER', 0, True),
        MetricInfo('Latency', 'Average', 'GAUGE', 4, False),
        MetricInfo('HTTPCode_ELB_4XX', 'Sum', 'COUNTER', 0, True),
        MetricInfo('HTTPCode_ELB_5XX', 'Sum', 'COUNTER', 0, True),
        MetricInfo('HTTPCode_Backend_2XX', 'Sum', 'COUNTER', 0, True),
        MetricInfo('HTTPCode_Backend_3XX', 'Sum', 'COUNTER', 0, True),
        MetricInfo('HTTPCode_Backend_4XX', 'Sum', 'COUNTER', 0, True),
        MetricInfo('HTTPCode_Backend_5XX', 'Sum', 'COUNTER', 0, True),
        MetricInfo('BackendConnectionErrors', 'Sum', 'COUNTER', 0, True),
        MetricInfo('SurgeQueueLength', 'Maximum', 'GAUGE', 0, True),
        MetricInfo('SpilloverCount', 'Sum', 'COUNTER', 0, True)
    ]

    def process_config(self):
        if self.config['enabled']:
            self.interval = self.config.as_int('interval')
            # Why is this?
            if self.interval % 60 != 0:
                raise Exception('Interval must be a multiple of 60 seconds: %s'
                                % self.interval)

        if ('access_key_id' in self.config
                and 'secret_access_key' in self.config):
            self.auth_kwargs = {
                'aws_access_key_id': self.config['access_key_id'],
                'aws_secret_access_key': self.config['secret_access_key']
            }
        else:
            # If creds not present, assume we're using IAM roles with
            # instance profiles. Boto will automatically take care of using
            # the creds from the instance metatdata.
            self.auth_kwargs = {}

    def check_boto(self):
        if not cloudwatch:
            self.log.error("boto module not found!")
            return False
        return True

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(ElbCollector, self).get_default_config()
        config.update({
            'path': 'elb',
            'regions': ['us-west-1'],
            'interval': 60,
            'format': '$zone.$elb_name.$metric_name',
        })
        return config

    def publish_delayed_metric(self, name, value, timestamp, raw_value=None,
                               precision=0, metric_type='GAUGE', instance=None):
        """
        Metrics may not be immediately available when querying cloudwatch.
        Hence, allow the ability to publish a metric from some the past given
        its timestamp.
        """
        # Get metric Path
        path = self.get_metric_path(name, instance)

        # Get metric TTL
        ttl = float(self.config['interval']) * float(
            self.config['ttl_multiplier'])

        # Create Metric
        metric = Metric(path, value, raw_value=raw_value, timestamp=timestamp,
                        precision=precision, host=self.get_hostname(),
                        metric_type=metric_type, ttl=ttl)

        # Publish Metric
        self.publish_metric(metric)

    def get_elb_names(self, region, config):
        """
        :param region: name of a region
        :param config: Collector config dict
        :return: list of elb names to query in the given region
        """
        # This function is ripe to be memoized but when ELBs are added/removed
        # dynamically over time, diamond will have to be restarted to pick
        # up the changes.
        region_dict = config.get('regions', {}).get(region, {})
        if 'elb_names' not in region_dict:
            elb_conn = boto.ec2.elb.connect_to_region(region,
                                                      **self.auth_kwargs)
            full_elb_names = \
                [elb.name for elb in elb_conn.get_all_load_balancers()]

            # Regular expressions for ELBs we DO NOT want to get metrics on.
            matchers = \
                [re.compile(regex) for regex in config.get('elbs_ignored', [])]

            # cycle through elbs get the list of elbs that don't match
            elb_names = []
            for elb_name in full_elb_names:
                if matchers and any([m.match(elb_name) for m in matchers]):
                    continue
                elb_names.append(elb_name)
        else:
            elb_names = region_dict['elb_names']
        return elb_names

    def process_stat(self, region, zone, elb_name, metric, stat, end_time):
        template_tokens = {
            'region': region,
            'zone': zone,
            'elb_name': elb_name,
            'metric_name': metric.name,
        }
        name_template = Template(self.config['format'])
        formatted_name = name_template.substitute(template_tokens)
        self.publish_delayed_metric(
            formatted_name,
            stat[metric.aws_type],
            metric_type=metric.diamond_type,
            precision=metric.precision,
            timestamp=time.mktime(utc_to_local(end_time).timetuple()))

    def process_metric(self, region_cw_conn, zone, start_time, end_time,
                       elb_name, metric):
        stats = region_cw_conn.get_metric_statistics(
            self.config['interval'],
            start_time,
            end_time,
            metric.name,
            namespace='AWS/ELB',
            statistics=[metric.aws_type],
            dimensions={
                'LoadBalancerName': elb_name,
                'AvailabilityZone': zone
            })

        # create a fake stat if the current metric should default to zero when
        # a stat is not returned. Cloudwatch just skips the metric entirely
        # instead of wasting space to store/emit a zero.
        if len(stats) == 0 and metric.default_to_zero:
            stats.append({
                u'Timestamp': start_time,
                metric.aws_type: 0.0,
                u'Unit': u'Count'
            })

        for stat in stats:
            self.process_stat(region_cw_conn.region.name, zone, elb_name,
                              metric, stat, end_time)

    def process_elb(self, region_cw_conn, zone, start_time, end_time, elb_name):
        for metric in self.metrics:
            self.process_metric(region_cw_conn, zone, start_time, end_time,
                                elb_name, metric)

    def process_zone(self, region_cw_conn, zone, start_time, end_time):
        for elb_name in self.get_elb_names(region_cw_conn.region.name,
                                           self.config):
            self.process_elb(region_cw_conn, zone, start_time, end_time,
                             elb_name)

    def process_region(self, region_cw_conn, start_time, end_time):
        for zone in get_zones(region_cw_conn.region.name, self.auth_kwargs):
            self.process_zone(region_cw_conn, zone, start_time, end_time)

    def collect(self):
        if not self.check_boto():
            return

        now = datetime.datetime.utcnow()
        end_time = now.replace(second=0, microsecond=0)
        start_time = end_time - datetime.timedelta(seconds=self.interval)

        for region in self.config['regions'].keys():
            region_cw_conn = cloudwatch.connect_to_region(region,
                                                          **self.auth_kwargs)
            self.process_region(region_cw_conn, start_time, end_time)
