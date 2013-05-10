# coding=utf-8

"""
Amazon SQS collector.

#### Dependencies

 * boto

"""

import diamond.collector
from boto import sqs

class SqsCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(SqsCollector,
                            self).get_default_config_help()
        config_help.update({
            'aws_access_key_id': 'AWS access key id',
            'aws_secret_access_key': 'AWS secret access key',
            'aws_region': 'AWS region',
            'sqs_queue': 'SQS queue name'
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(SqsCollector, self).get_default_config()
        config.update({
            'path': 'sqs',
        })
        return config

    def collect(self):
        conn = sqs.connect_to_region(self.config['aws_region'],
                                     aws_access_key_id=self.config['aws_access_key_id'],
                                     aws_secret_access_key=self.config['aws_secret_access_key'])
        queue = conn.get_queue(self.config['sqs_queue'])
        attribs = ['ApproximateNumberOfMessages',
                   'ApproximateNumberOfMessagesNotVisible',
                   'ApproximateNumberOfMessagesDelayed',
                   'CreatedTimestamp',
                   'DelaySeconds',
                   'LastModifiedTimestamp',
                   'MaximumMessageSize',
                   'MessageRetentionPeriod',
                   'ReceiveMessageWaitTimeSeconds',
                   'VisibilityTimeout']

        for attrib in attribs:
            d = queue.get_attributes(attrib)
	    self.publish('%s.%s.%s' % (self.config['aws_region'], self.config['sqs_queue'], attrib), d[attrib])
