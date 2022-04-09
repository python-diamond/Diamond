# coding=utf-8
"""
Output the collected values to AWS CloudWatch

Automatically adds the InstanceId Dimension

#### Dependencies

 * [boto](http://boto.readthedocs.org/en/latest/index.html)

#### Configuration

Enable this handler

 * handers = diamond.handler.cloudwatch.cloudwatchHandler

Example Config:

[[cloudwatchHandler]]
region = us-east-1

[[[LoadAvg01]]]
collect_by_instance = True
collect_without_dimension = False
collector = loadavg
metric = 01
name = Avg01
namespace = MachineLoad
unit = None

[[[LoadAvg05]]]
collect_by_instance = True
collect_without_dimension = False
collector = loadavg
metric = 05
name = Avg05
namespace = MachineLoad
unit = None
[[[[dimensions]]]]
environment = dev

"""

import sys
import datetime

from diamond.handler.Handler import Handler
from configobj import Section

try:
    import boto
    import boto.ec2.cloudwatch
    import boto.utils
except ImportError:
    boto = None


class cloudwatchHandler(Handler):
    """
      Implements the abstract Handler class
      Sending data to a AWS CloudWatch
    """

    def __init__(self, config=None):
        """
          Create a new instance of cloudwatchHandler class
        """

        # Initialize Handler
        Handler.__init__(self, config)

        if not boto:
            self.log.error(
                "CloudWatch: Boto is not installed, please install boto.")
            return

        # Initialize Data
        self.connection = None

        # Initialize Options
        self.region = self.config['region']

        instance_metadata = boto.utils.get_instance_metadata()
        if 'instance-id' in instance_metadata:
            self.instance_id = instance_metadata['instance-id']
            self.log.debug("Setting InstanceId: " + self.instance_id)
        else:
            self.instance_id = None
            self.log.error('CloudWatch: Failed to load instance metadata')

        self.valid_config = ('region', 'collector', 'metric', 'namespace',
                             'name', 'unit', 'collect_by_instance',
                             'collect_without_dimension', 'dimensions')

        self.rules = []
        for key_name, section in self.config.items():
            if section.__class__ is Section:
                keys = section.keys()
                rules = self.get_default_rule_config()
                for key in keys:
                    if key not in self.valid_config:
                        self.log.warning("invalid key %s in section %s",
                                         key, section.name)
                    else:
                        rules[key] = section[key]

                self.rules.append(rules)

        # Create CloudWatch Connection
        self._bind()

    def get_default_rule_config(self):
        """
        Return the default config for a rule
        """
        config = {}
        config.update({
            'collector': '',
            'metric': '',
            'namespace': '',
            'name': '',
            'unit': 'None',
            'collect_by_instance': True,
            'collect_without_dimension': False,
            'dimensions': {}
        })
        return config

    def get_default_config_help(self):
        """
        Returns the help text for the configuration options for this handler
        """
        config = super(cloudwatchHandler, self).get_default_config_help()

        config.update({
            'region': 'AWS region',
            'metric': 'Diamond metric name',
            'namespace': 'CloudWatch metric namespace',
            'name': 'CloudWatch metric name',
            'unit': 'CloudWatch metric unit',
            'collector': 'Diamond collector name',
            'collect_by_instance': 'Collect metrics for instances separately',
            'collect_without_dimension': 'Collect metrics without dimension',
            'dimensions': 'Additional dimensions to pass (Up to 10)'
        })

        return config

    def get_default_config(self):
        """
        Return the default config for the handler
        """
        config = super(cloudwatchHandler, self).get_default_config()

        config.update({
            'region': 'us-east-1',
            'collector': 'loadavg',
            'metric': '01',
            'namespace': 'MachineLoad',
            'name': 'Avg01',
            'unit': 'None',
            'collect_by_instance': True,
            'collect_without_dimension': False
        })

        return config

    def _bind(self):
        """
           Create CloudWatch Connection
        """

        self.log.debug(
            "CloudWatch: Attempting to connect to CloudWatch at Region: %s",
            self.region)
        try:
            self.connection = boto.ec2.cloudwatch.connect_to_region(
                self.region)
            self.log.debug(
                "CloudWatch: Succesfully Connected to CloudWatch at Region: %s",
                self.region)
        except boto.exception.EC2ResponseError:
            self.log.error('CloudWatch: CloudWatch Exception Handler: ')

    def __del__(self):
        """
          Destroy instance of the cloudWatchHandler class
        """
        try:
            self.connection = None
        except AttributeError:
            pass

    def process(self, metric):
        """
          Process a metric and send it to CloudWatch
        """
        if not boto:
            return

        collector = str(metric.getCollectorPath())
        metricname = str(metric.getMetricPath())

        # Send the data as ......

        for rule in self.rules:
            self.log.debug(
                "Comparing Collector: [%s] with (%s) "
                "and Metric: [%s] with (%s)",
                str(rule['collector']),
                collector,
                str(rule['metric']),
                metricname
            )

            if ((str(rule['collector']) == collector and
                 str(rule['metric']) == metricname)):

                if rule['collect_by_instance'] and self.instance_id:
                    dimensions = rule['dimensions']
                    dimensions['InstanceId'] = self.instance_id
                    self.send_metrics_to_cloudwatch(
                        rule,
                        metric,
                        dimensions)

                if rule['collect_without_dimension']:
                    self.send_metrics_to_cloudwatch(
                        rule,
                        metric,
                        {})

    def send_metrics_to_cloudwatch(self, rule, metric, dimensions):
        """
          Send metrics to CloudWatch for the given dimensions
        """

        timestamp = datetime.datetime.utcfromtimestamp(metric.timestamp)

        self.log.debug(
            "CloudWatch: Attempting to publish metric: %s to %s "
            "with value (%s) for dimensions %s @%s",
            rule['name'],
            rule['namespace'],
            str(metric.value),
            str(dimensions),
            str(metric.timestamp)
        )

        try:
            self.connection.put_metric_data(
                str(rule['namespace']),
                str(rule['name']),
                str(metric.value),
                timestamp, str(rule['unit']),
                dimensions)
            self.log.debug(
                "CloudWatch: Successfully published metric: %s to"
                " %s with value (%s) for dimensions %s",
                rule['name'],
                rule['namespace'],
                str(metric.value),
                str(dimensions))
        except AttributeError as e:
            self.log.error(
                "CloudWatch: Failed publishing - %s ", str(e))
        except Exception as e:  # Rough connection re-try logic.
            self.log.error(
                "CloudWatch: Failed publishing - %s\n%s ",
                str(e),
                str(sys.exc_info()[0]))
            self._bind()
