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

[[[LoadAvg01]]] # this example sends metrics for an autoscaling group
collector = loadavg
metric = 01
namespace = "AWS/AutoScaling"
autoscaling = true
name = Avg01
unit = None

[[[LoadAvg05]]] # this example sends metrics for a single instance
collector = loadavg
metric = 05
namespace = MachineLoad
name = Avg05
unit = None
"""

import sys
import datetime

from diamond.handler.Handler import Handler
from configobj import Section

try:
    import boto
    import boto.ec2
    import boto.ec2.cloudwatch
    import boto.utils
except ImportError:
    boto = None

from json import load

class InstanceTypeError(Exception):
    """
    This is thrown when the user tries to publish a metric to the
    wrong instance type

    Example: Trying to publish a metric to AutoScaling for an
             instance that is not in an AutoScaling Group
    """
    pass


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
        self.cloudwatch = None
        self.cached_aws_info = None

        try:
            self.cached_aws_info = self.config['awsinfo']
            self.log.debug("Found cached AWS Instance details, I won't call AWS for them")
        except KeyError:
            self.log.debug("Proceeding by calling AWS for instance details")

        if self.cached_aws_info:
            with open(self.config['awsinfo'], 'r') as awsinfo:
                info = load(awsinfo)
                self.instance_id = info['instance']
                self.autoscaling_group_name = info['autoscaling_group_name']
                self.region = info['region']
                self.log.debug("Grabbed AWS Info from file")
        else:
            # Initialize Options
            self.region = self.config['region']
            instances = boto.utils.get_instance_metadata()
            if 'instance-id' not in instances:
                self.log.error('CloudWatch: Failed to load instance metadata')
                return
            self.instance_id = instances['instance-id']
            self.autoscaling_group_name = None
            self.log.debug("Grabbed AWS Info from Boto")
        self.log.debug("Setting InstanceId: " + self.instance_id)

        self.valid_config = ('region',
                             'collector',
                             'metric',
                             'namespace',
                             'name',
                             'unit',
                             'autoscaling',
                             'awsinfo')

        self.rules = []
        for _, section in self.config.items():
            if section.__class__ is Section:
                keys = section.keys()
                rules = {}
                for key in keys:
                    if key not in self.valid_config:
                        self.log.warning("invalid key %s in section %s",
                                         key, section.name)
                    else:
                        rules[key] = section[key]

                self.rules.append(rules)

        # Create CloudWatch Connection
        self._bind()

    def get_default_config_help(self):
        """
        Returns the help text for the configuration options for this handler
        """
        config = super(cloudwatchHandler, self).get_default_config_help()

        config.update({
            'region': '',
            'metric': '',
            'namespace': '',
            'name': '',
            'unit': '',
            'collector': '',
            'autoscaling': '',
            'awsinfo': ''
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
            'autoscaling': 'false',
            'awsinfo': None
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
            self.ec2 = boto.ec2.connect_to_region(self.region)
            self.cloudwatch = boto.ec2.cloudwatch.connect_to_region(
                self.region)
            self.log.debug(
                "CloudWatch: Succesfully Connected to CloudWatch Region: %s",
                self.region)
        except boto.exception.EC2ResponseError:
            self.log.error('CloudWatch: CloudWatch Exception Handler: ')

    def __del__(self):
        """
          Destroy instance of the cloudWatchHandler class
        """
        try:
            self.cloudwatch = None
        except AttributeError:
            pass

    def process(self, metric):
        """
          Process a metric and send it to CloudWatch
          :param metric: Object
        """
        if not boto:
            return

        collector = str(metric.getCollectorPath())
        metricname = str(metric.getMetricPath())
        timestamp = datetime.datetime.fromtimestamp(metric.timestamp)

        try:
            if self.config['autoscaling']:
                if not self.autoscaling_group_name:
                    self.log.debug("Grabbing AutoScaling group name from Boto")
                    instances = self.ec2.get_only_instances(["%s" % self.instance_id])
                    inst = instances[0]
                    self.log.debug(inst.tags['aws:autoscaling:groupName'])
                    autoscaling_group = inst.tags['aws:autoscaling:groupName']
                else:
                    self.log.debug("AutoScaling group name read from cache, sending to it.")
                    autoscaling_group = self.autoscaling_group_name
        except KeyError:
            raise InstanceTypeError(
                'This instance is not in an AutoScaling group'
            )

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
                self.log.debug(
                    "CloudWatch: Attempting to publish metric: %s to %s "
                    "with value (%s) @%s",
                    rule['name'],
                    rule['namespace'],
                    str(metric.value),
                    str(metric.timestamp)
                )
                try:
                    if self.config['autoscaling']:
                        target = {'AutoScalingGroupName': autoscaling_group}
                        self.log.debug(
                            'Cloudwatch: Publishing metric to AutoScaling'
                        )
                    else:
                        target = {'InstanceId': self.instance_id}
                        self.log.debug(
                            'Cloudwatch: Publishing metric to Instance'
                        )

                    self.cloudwatch.put_metric_data(
                        str(rule['namespace']),
                        str(rule['name']),
                        str(metric.value),
                        timestamp, str(rule['unit']),
                        target)

                    self.log.debug(
                        "CloudWatch: Successfully published metric: %s to"
                        " %s with value (%s)",
                        rule['name'],
                        rule['namespace'],
                        str(metric.value)
                    )
                except AttributeError as err:
                    self.log.error(
                        "CloudWatch: Failed publishing - %s ", str(err))
                except Exception:  # Rough connection re-try logic.
                    self.log.error(
                        "CloudWatch: Failed publishing - %s ",
                        str(sys.exc_info()[0]))
                    self._bind()
