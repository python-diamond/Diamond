# coding=utf-8
"""
Output the collected values to AWS CloudWatch

Automatically adds the InstanceId Dimension

#### Dependencies

 * [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)

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
import urllib.request

from . Handler import Handler
from configobj import Section

try:
    import boto3
    import botocore.exceptions
except ImportError:
    boto3 = None

METADATA_URL = 'http://169.254.169.254/latest'


def get_instance_id(timeout=2):
    """
    Return the EC2 instance id from the instance metadata service (IMDSv2),
    or None if it cannot be retrieved.
    """
    try:
        token_request = urllib.request.Request(
            METADATA_URL + '/api/token', method='PUT',
            headers={'X-aws-ec2-metadata-token-ttl-seconds': '60'})
        with urllib.request.urlopen(token_request, timeout=timeout) as resp:
            token = resp.read().decode()
        id_request = urllib.request.Request(
            METADATA_URL + '/meta-data/instance-id',
            headers={'X-aws-ec2-metadata-token': token})
        with urllib.request.urlopen(id_request, timeout=timeout) as resp:
            return resp.read().decode()
    except OSError:
        return None


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

        if not boto3:
            self.log.error(
                "CloudWatch: Boto3 is not installed, please install boto3.")
            return

        # Initialize Data
        self.connection = None

        # Initialize Options
        self.region = self.config['region']

        self.instance_id = get_instance_id()
        if self.instance_id:
            self.log.debug("Setting InstanceId: " + self.instance_id)
        else:
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
            self.connection = boto3.client('cloudwatch',
                                           region_name=self.region)
            self.log.debug(
                "CloudWatch: Succesfully Connected to CloudWatch at Region: %s",
                self.region)
        except botocore.exceptions.BotoCoreError:
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
        if not boto3:
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

        timestamp = datetime.datetime.fromtimestamp(
            metric.timestamp, datetime.timezone.utc)

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
                Namespace=str(rule['namespace']),
                MetricData=[{
                    'MetricName': str(rule['name']),
                    'Dimensions': [{'Name': str(name), 'Value': str(value)}
                                   for name, value in dimensions.items()],
                    'Timestamp': timestamp,
                    'Value': float(metric.value),
                    'Unit': str(rule['unit']),
                }])
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
