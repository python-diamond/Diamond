# coding=utf-8

"""
The ELB collector collects metrics for one or more Amazon AWS ELBs

#### Configuration

Below is an example configuration for the ELBCollector.
You can specify an arbitrary amount of regions

```
    enabled = true
    interval = 60
    access_key_id = ...
    secret_access_key = ...

    [[regions]]
    [us-west-1]
    # Optional - omit to collect from all elbs
    elbs = elb1, elb2, ...

    [us-west-2]
    ...

```

#### Dependencies

 * boto

"""
import datetime

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
        ('SpilloverCount', 'Sum')]

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(ElbCollector, self).get_default_config()
        config.update({
            'path': 'elb',
            'regions': ['us-west-1']
        })
        return config

    def _get_all_elbs(self, region, **auth_kwargs):
        """
        :return: List of all elbs in the given region
        """
        elb_conn = boto.ec2.elb.connect_to_region(region, **auth_kwargs)
        return [elb.name for elb in elb_conn.get_all_load_balancers()]

    def collect(self):

        self.log.debug('collect called!')

        if not cloudwatch:
            self.log.error("boto module not found!")
            return

        end_time = datetime.datetime.now()
        start_time = end_time - datetime.timedelta(minutes=1)

        auth_kwargs = {
            'aws_access_key_id' : self.config['access_key_id'],
            'aws_secret_access_key' : self.config['secret_access_key']
        }

        for (region, region_cfg) in self.config['regions'].items():
            if 'elbs' not in region_cfg:
                elb_names = self._get_all_elbs(region, **auth_kwargs)
            else:
                elb_names = region_cfg['elbs']

            ec2_conn = boto.ec2.connect_to_region(region, **auth_kwargs)
            zones = [zone.name for zone in ec2_conn.get_all_zones()]

            for elb_name in elb_names:
                conn = cloudwatch.connect_to_region(region, **auth_kwargs)

                for metric_name, statistic in self.metrics:

                    for zone in zones:
                        # NOTE: Dimensioning by elb name only gives wonky stats (1.6667 HealthyHosts for example).
                        #       Have to also include region for legit numbers and aggregate by region downstream.
                        stats = conn.get_metric_statistics(
                            60,
                            start_time,
                            end_time,
                            metric_name,
                            namespace='AWS/ELB',
                            statistics=[statistic],
                            dimensions={'LoadBalancerName':elb_name, 'AvailabilityZone' : zone})

                        published_name = '%s.%s.%s' % (zone, elb_name, metric_name)

                        num_stats = len(stats)
                        if num_stats == 0:
                            # no statistic available for this metric, default to zero
                            metric_value = 0
                        else:
                            metric_value = stats[-1][statistic]
                            if num_stats > 1:
                                self.log.warn('More than one statistic returned for %s:%s' % (published_name, stats))
                        self.log.debug("%s %s" % (published_name, metric_value))
                        #if stats:
                        #    print stats[-1]
                        self.publish(published_name, metric_value)
