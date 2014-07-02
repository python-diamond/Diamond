# coding=utf-8

"""
The ELB collector collects metrics for one or more Amazon AWS ELBs

#### Configuration

Below is an example configuration for the ELBCollector.
You can specify an arbitrary amount of regions

```
    enabled = true
    interval = 60
    # max number of delayed metrics to tolerate
    max_delayed = 10

    # Optional
    access_key_id = ...
    secret_access_key = ...

    # Optional - Available keys: region, zone, elb_name, metric_name
    format = $elb_name.$zone.$metric_name

    # Optional - list of regular expressions used to ignore ELBs
    elbs_ignored = ^elb-a$, .*-test$, $test-.*

    [[regions]]

    [us-west-1]
    # Optional - queries all elbs if omitted
    elb_names = elb1, elb2, ...

    [us-west-2]
    ...

```

#### Dependencies

 * boto

"""
import calendar
import datetime
import functools
import re
import time
from collections import defaultdict
from string import Template

import diamond.collector
from diamond.metric import Metric

try:
    import boto.ec2.elb
    from boto.ec2 import cloudwatch
    from boto.exception import NoAuthHandlerFound
    cloudwatch  # Pyflakes
except ImportError:
    cloudwatch = False


class memoized(object):
    """Decorator that caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned, and
    the function is not re-evaluated.

    Based upon from http://wiki.python.org/moin/PythonDecoratorLibrary#Memoize
    Nota bene: this decorator memoizes /all/ calls to the function.  For a memoization
    decorator with limited cache size, consider:
    http://code.activestate.com/recipes/496879-memoize-decorator-function-with-cache-size-limit/
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
def get_zones(region, auth_dict, log):
    """
    :param region: region to get the availability zones for
    :param auth_dict: Used to authenticate with EC2.
        Empty dict if using instance profiles.
    :return: list of availability zones
    """
    try:
        ec2_conn = boto.ec2.connect_to_region(region, **auth_dict)
    except NoAuthHandlerFound, e:
        log.error(e)
    return [zone.name for zone in ec2_conn.get_all_zones()]


@memoized
def get_elb_names(region, config, auth_dict):
    """
    :param region: name of a region
    :param config: Collector config dict
    :param auth_dict: Used to authenticate with EC2.
        Empty dict if using instance profiles.
    :return: list of elb names to query in the given region
    """
    if 'elb_names' not in config['region']:
        elb_conn = boto.ec2.elb.connect_to_region(region, **auth_dict)
        full_elb_names = [elb.name for elb in elb_conn.get_all_load_balancers()]

        # Regular expressions for ELBs we DO NOT want to get metrics on.
        matchers = [re.compile(regex) for regex in config.get('elbs_ignored', [])]

        # cycle through elbs get the list of elbs that don't match
        elb_names = []
        for elb_name in full_elb_names:
            if matchers and any([m.match(elb_name) for m in matchers]):
                continue
            elb_names.append(elb_name)
    else:
        elb_names = config.get('region',{}).get('elb_names',[])
    return elb_names


def handle_defaults(stats, default_to_zero, span_start, metric_stat_type):
    # create a fake stat if the current metric should default to zero when
    # a stat is not returned. Cloudwatch just skips the metric entirely
    # instead of wasting space to store/emit a zero.
    if len(stats) == 0 and default_to_zero:
        stats.append({
            u'Timestamp': span_start,
            metric_stat_type: 0.0,
            u'Unit': u'Count'
        })


class ElbCollector(diamond.collector.Collector):

    # (aws metric name, aws statistic type, diamond metric type, diamond
    # precision, emit zero when no value available)
    metrics = [
        ('HealthyHostCount', 'Average', 'GAUGE', 0, False),
        ('UnHealthyHostCount', 'Average', 'GAUGE', 0, False),
        ('RequestCount', 'Sum', 'COUNTER', 0, True),
        ('Latency', 'Average', 'GAUGE', 4, False),
        ('HTTPCode_ELB_4XX', 'Sum', 'COUNTER', 0, True),
        ('HTTPCode_ELB_5XX', 'Sum', 'COUNTER', 0, True),
        ('HTTPCode_Backend_2XX', 'Sum', 'COUNTER', 0, True),
        ('HTTPCode_Backend_3XX', 'Sum', 'COUNTER', 0, True),
        ('HTTPCode_Backend_4XX', 'Sum', 'COUNTER', 0, True),
        ('HTTPCode_Backend_5XX', 'Sum', 'COUNTER', 0, True),
        ('BackendConnectionErrors', 'Sum', 'COUNTER', 0, True),
        ('SurgeQueueLength', 'Maximum', 'GAUGE', 0, True),
        ('SpilloverCount', 'Sum', 'COUNTER', 0, True)
    ]

    def __init__(self, config, handlers):
        super(ElbCollector, self).__init__(config, handlers)

        def setup_creds():
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

        if self.config['enabled']:
            self.interval = self.config.as_int('interval')
            if self.interval % 60 != 0:
                raise Exception('Interval must be a multiple of 60 seconds: %s'
                                % self.interval)
        setup_creds()
        self.max_delayed = self.config.as_int('max_delayed')

        # key = tuple(zone, elb_name, metric_name)
        # value = list of tuple(start_time, end_time)
        self.history = defaultdict(list)

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
            'max_delayed': 10,
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

    def append_to_history(self, zone, elb_name, metric_name, tick):
        metric_history = self.history[(zone, elb_name, metric_name)]
        metric_history.append(tick)
        # only keep latest max_delayed metrics in history
        if len(metric_history) > self.max_delayed:
            del metric_history[0]
        return metric_history

    def process_tick(self, region, zone, elb_name, metric, stat, tick):
        metric_name, metric_stat_type, metric_type, metric_precision, default_to_zero = metric
        tick_start, tick_end = tick

        if stat['Timestamp'] != tick_start:
            return False

        template_tokens = {
            'region': region,
            'zone': zone,
            'elb_name': elb_name,
            'metric_name': metric_name,
        }
        name_template = Template(self.config['format'])
        formatted_name = name_template.substitute(template_tokens)
        self.publish_delayed_metric(
            formatted_name,
            stat[metric_stat_type],
            metric_type=metric_type,
            precision=metric_precision,
            timestamp=time.mktime(utc_to_local(tick_end).timetuple()))
        return True

    def process_stat(self, region, zone, elb_name, metric, stat, metric_history):
        metrics_to_delete = []
        for index, tick in enumerate(metric_history):
            metric_received = self.process_tick(region, zone, elb_name, metric, stat, tick)
            if metric_received:
                metrics_to_delete.append(index)

        # TODO: metric_history has to be contiguous! if not, we have problems!
        for index in reversed(metrics_to_delete):
            del metric_history[index]

    def process_metric(self, region, zone, start_time, end_time, elb_name, metric):
        metric_name, metric_stat_type, metric_type, metric_precision, default_to_zero = metric

        tick = (start_time, end_time)
        metric_history = self.append_to_history(zone, elb_name, metric_name, tick)
        span_start, _ = metric_history[0]
        _, span_end = metric_history[-1]
        cw_conn = cloudwatch.connect_to_region(region, **self.auth_kwargs)

        # get stats for the span of history for which we don't have values
        stats = cw_conn.get_metric_statistics(
            self.config['interval'],
            span_start,
            span_end,
            metric_name,
            namespace='AWS/ELB',
            statistics=[metric_stat_type],
            dimensions={
                'LoadBalancerName': elb_name,
                'AvailabilityZone': zone
            })

        #self.log.debug('history = %s' % metric_history)
        #self.log.debug('stats = %s' % stats)

        handle_defaults(stats, default_to_zero, span_start, metric_stat_type)

        # match up each individual stat to what we have in
        # history and publish it.
        for stat in stats:
            self.process_stat(region, zone, elb_name, metric, stat, metric_history)

    def process_elb(self, region, zone, start_time, end_time, elb_name):
        for metric in self.metrics:
            self.process_metric(region, zone, start_time, end_time, elb_name, metric)

    def process_zone(self, region, zone, start_time, end_time):
        for elb_name in get_elb_names(region, self.config):
            self.process_elb(region, zone, start_time, end_time, elb_name)

    def process_region(self, region, start_time, end_time):
        for zone in self.get_zones(region):
            self.process_zone(region, zone, start_time, end_time)

    def collect(self):
        if not self.check_boto():
            return

        now = datetime.datetime.utcnow()
        end_time = now.replace(second=0, microsecond=0)
        start_time = end_time - datetime.timedelta(seconds=self.interval)

        for region in self.config['regions'].keys():
            self.process_region(region, start_time, end_time)