# coding=utf-8

"""
The SQS collector collects metrics for one or more Amazon AWS SQS queues

#### Configuration

Below is an example configuration for the SQSCollector.
You can specify an arbitrary amount of regions

```
    enabled = True
    interval = 60

    [regions]
    [[region-code]]
    access_key_id = '...'
    secret_access_key = '''
    queues = queue_name[,queue_name2[,..]]

```

Note: If you modify the SQSCollector configuration, you will need to
restart diamond.

#### Dependencies

 * boto

"""

import diamond.collector
try:
    from boto import sqs
except ImportError:
    sqs = False


class SqsCollector(diamond.collector.Collector):

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
        if not sqs:
            self.log.error("boto module not found!")
            return
        for (region, region_cfg) in self.config['regions'].items():
            assert 'access_key_id' in region_cfg
            assert 'secret_access_key' in region_cfg
            assert 'queues' in region_cfg
            queues = region_cfg['queues'].split(',')
            for queue_name in queues:
                conn = sqs.connect_to_region(
                    region,
                    aws_access_key_id=region_cfg['access_key_id'],
                    aws_secret_access_key=region_cfg['secret_access_key'],
                )
                queue = conn.get_queue(queue_name)

                for attrib in attribs:
                    d = queue.get_attributes(attrib)
                    self.publish(
                        '%s.%s.%s' % (region, queue_name, attrib),
                        d[attrib]
                    )
