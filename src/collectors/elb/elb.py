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
from string import Template

import diamond.collector
try:
    import boto.ec2.elb
    from boto.ec2 import cloudwatch
    cloudwatch  # Pyflakes
except ImportError:
    cloudwatch = False


class ElbCollector(diamond.collector.Collector):

    metrics = [
        ('HealthyHostCount', 'Average'),
        ('UnhealthyHostCount', 'Average'),
        ('RequestCount', 'Sum'),
        ('Latency', 'Average'),
        ('HTTPCode_ELB_4XX', 'Sum'),
        ('HTTPCode_ELB_5XX', 'Sum'),
        ('HTTPCode_Backend_2XX', 'Sum'),
        ('HTTPCode_Backend_3XX', 'Sum'),
        ('HTTPCode_Backend_4XX', 'Sum'),
        ('HTTPCode_Backend_5XX', 'Sum'),
        ('BackendConnectionErrors', 'Sum'),
        ('SurgeQueueLength', 'Maximum'),
        ('SpilloverCount', 'Sum')
    ]

    def __init__(self, config, handlers):
        super(ElbCollector, self).__init__(config, handlers)

        def validate_interval():
            self.interval = self.config.as_int('interval')
            if self.interval % 60 != 0:
                raise Exception('Interval must be a multiple of 60 seconds: %s' % self.interval)

        def setup_creds():
            if 'access_key_id' in self.config and 'secret_access_key' in self.config:
                self.auth_kwargs = {
                    'aws_access_key_id' : self.config['access_key_id'],
                    'aws_secret_access_key' : self.config['secret_access_key']
                }
            else:
                # If creds not present, assume we're using IAM roles with instance profiles.
                # Boto will automatically take care of using the creds from the instance metatdata.
                self.auth_kwargs = {}

        def cache_zones():
            self.zones_by_region = {}
            for region in self.config['regions'].keys():
                ec2_conn = boto.ec2.connect_to_region(region, **self.auth_kwargs)
                self.zones_by_region[region] = [zone.name for zone in ec2_conn.get_all_zones()]

        self.check_boto()
        validate_interval()
        setup_creds()
        cache_zones()

    def check_boto(self):
        if not cloudwatch:
            self.log.error("boto module not found!")
            return

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(ElbCollector, self).get_default_config()
        config.update({
            'path': 'elb',
            'regions': ['us-west-1'],
            'interval': 60,
            'format' : '$zone.$elb_name.$metric_name',
        })
        return config

    def get_elb_names(self, region, region_cfg):
        """
        :return: List of elb names to query in the given region
        """
        if 'elb_names' not in region_cfg:
            elb_conn = boto.ec2.elb.connect_to_region(region, **self.auth_kwargs)
            elb_names = [elb.name for elb in elb_conn.get_all_load_balancers()]
        else:
            elb_names = region_cfg['elb_names']
        return elb_names

    def collect(self):
        self.check_boto()

        end_time = datetime.datetime.now()
        start_time = end_time - datetime.timedelta(seconds=self.interval)

        for (region, region_cfg) in self.config['regions'].items():
            for elb_name in self.get_elb_names(region, region_cfg):
                conn = cloudwatch.connect_to_region(region, **self.auth_kwargs)
                for metric_name, statistic in self.metrics:
                    for zone in self.zones_by_region[region]:
                        # NOTE: Dimensioning by elb name only gives wonky stats (1.6667 HealthyHosts for example).
                        #       Have to also include region for legit numbers and aggregate by region downstream.
                        stats = conn.get_metric_statistics(
                            self.config['interval'],
                            start_time,
                            end_time,
                            metric_name,
                            namespace='AWS/ELB',
                            statistics=[statistic],
                            dimensions={'LoadBalancerName':elb_name, 'AvailabilityZone' : zone})

                        template_tokens = {
                            'region'      : region,
                            'zone'        : zone,
                            'elb_name'    : elb_name,
                            'metric_name' : metric_name,
                        }
                        name_template = Template(self.config['format'])
                        name = name_template.substitute(template_tokens)

                        num_stats = len(stats)
                        if num_stats == 0:
                            # no statistic available for this metric, default to zero
                            metric_value = 0
                        else:
                            metric_value = stats[-1][statistic]
                            if num_stats > 1:
                                self.log.warn('More than one statistic returned for %s:%s' % (name, stats))
                        self.publish(name, metric_value)
