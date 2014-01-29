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
import datetime
import time
from string import Template

import diamond.collector
from diamond.metric import Metric

try:
    import boto.ec2.elb
    from boto.ec2 import cloudwatch
    cloudwatch  # Pyflakes
except ImportError:
    cloudwatch = False


class ElbCollector(diamond.collector.Collector):

    # (aws metric name, aws statistic type, diamond metric type, diamond
    # precision)
    metrics = [
        ('HealthyHostCount', 'Average', 'GAUGE', 0),
        ('UnhealthyHostCount', 'Average', 'GAUGE', 0),
        ('RequestCount', 'Sum', 'COUNTER', 0),
        ('Latency', 'Average', 'GAUGE', 4),
        ('HTTPCode_ELB_4XX', 'Sum', 'COUNTER', 0),
        ('HTTPCode_ELB_5XX', 'Sum', 'COUNTER', 0),
        ('HTTPCode_Backend_2XX', 'Sum', 'COUNTER', 0),
        ('HTTPCode_Backend_3XX', 'Sum', 'COUNTER', 0),
        ('HTTPCode_Backend_4XX', 'Sum', 'COUNTER', 0),
        ('HTTPCode_Backend_5XX', 'Sum', 'COUNTER', 0),
        ('BackendConnectionErrors', 'Sum', 'COUNTER', 0),
        ('SurgeQueueLength', 'Maximum', 'GAUGE', 0),
        ('SpilloverCount', 'Sum', 'COUNTER', 0)
    ]

    def __init__(self, config, handlers):
        super(ElbCollector, self).__init__(config, handlers)

        def validate_interval():
            self.interval = self.config.as_int('interval')
            if self.interval % 60 != 0:
                raise Exception('Interval must be a multiple of 60 seconds: %s'
                                % self.interval)

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

        def cache_zones():
            self.zones_by_region = {}
            for region in self.config['regions'].keys():
                ec2_conn = boto.ec2.connect_to_region(region,
                                                      **self.auth_kwargs)
                self.zones_by_region[region] = [
                    zone.name for zone in ec2_conn.get_all_zones()]

        if not self.check_boto():
            return
        validate_interval()
        setup_creds()
        cache_zones()
        self.max_delayed = self.config.as_int('max_delayed')
        self.history = dict()

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

    def get_elb_names(self, region, region_cfg):
        """
        :return: List of elb names to query in the given region
        """
        if 'elb_names' not in region_cfg:
            elb_conn = boto.ec2.elb.connect_to_region(region,
                                                      **self.auth_kwargs)
            elb_names = [elb.name for elb in elb_conn.get_all_load_balancers()]
        else:
            elb_names = region_cfg['elb_names']
        return elb_names

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

    def collect(self):
        self.check_boto()

        now = datetime.datetime.now()
        end_time = now.replace(second=0, microsecond=0)
        start_time = end_time - datetime.timedelta(seconds=self.interval)

        for (region, region_cfg) in self.config['regions'].items():
            conn = cloudwatch.connect_to_region(region, **self.auth_kwargs)
            for elb_name in self.get_elb_names(region, region_cfg):
                for (metric_name, statistic,
                        metric_type, precision) in self.metrics:
                    for zone in self.zones_by_region[region]:

                        metric_key = (zone, elb_name, metric_name)
                        if metric_key not in self.history:
                            self.history[metric_key] = list()
                        current_history = self.history[metric_key]

                        tick = (start_time, end_time)
                        current_history.append(tick)

                        # only keep latest MAX_TICKS
                        if len(current_history) > self.max_delayed:
                            del current_history[0]

                        span_start, _ = current_history[0]
                        _, span_end = current_history[-1]

                        # get stats for the span of history for which we don't
                        # have values
                        stats = conn.get_metric_statistics(
                            self.config['interval'],
                            span_start,
                            span_end,
                            metric_name,
                            namespace='AWS/ELB',
                            statistics=[statistic],
                            dimensions={'LoadBalancerName': elb_name,
                                        'AvailabilityZone': zone})

                        #self.log.debug('history = %s' % current_history)
                        #self.log.debug('stats = %s' % stats)

                        # match up each individual stat to what we have in
                        # history and publish it.
                        for stat in stats:
                            ts = stat['Timestamp']
                            # TODO: maybe use a dict for matching
                            for i, tick in enumerate(current_history):
                                tick_start, tick_end = tick
                                if ts == tick_start:
                                    #self.log.debug(tick)
                                    #self.log.debug(stat)
                                    del current_history[i]

                                    template_tokens = {
                                        'region': region,
                                        'zone': zone,
                                        'elb_name': elb_name,
                                        'metric_name': metric_name,
                                    }
                                    name_template = Template(
                                        self.config['format'])
                                    formatted_name = name_template.substitute(
                                        template_tokens)
                                    self.publish_delayed_metric(
                                        formatted_name,
                                        stat[statistic],
                                        metric_type=metric_type,
                                        precision=precision,
                                        timestamp=time.mktime(
                                            tick_end.timetuple()))
                                    break
