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
    queues = queue_name[,queue_name2[,..]]
    # Optional - assumes IAM role with instance profile if not provided.
    access_key_id = '...'
    secret_access_key = '''

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
            assert 'queues' in region_cfg
            auth_kwargs = _get_auth_kwargs(config=region_cfg)
            queues = region_cfg['queues'].split(',')
            for queue_name in queues:
                conn = sqs.connect_to_region(region, **auth_kwargs)
                queue = conn.get_queue(queue_name)
                for attrib in attribs:
                    d = queue.get_attributes(attrib)
                    self.publish(
                        '%s.%s.%s' % (region, queue_name, attrib),
                        d[attrib]
                    )


def _get_auth_kwargs(config):
    """Generate the kwargs for the AWS keys from a configuration dictionary.

    If credentials are not present in the config, then assume that
    we're using IAM roles with instance profiles. :mod:`boto` will
    automatically take care of using the credentials from the instance
    metadata if not provided with kwargs.

    :param config: The configuration to use when looking for explicitly
        provided AWS credentials.
    :type config: dict

    :returns: The kwargs for use with :mod:`boto` connect functions.
    :rtype: dict
    """
    if not ('access_key_id' in config and 'secret_access_key' in config):
        return {}
    return {
        'aws_access_key_id': config['access_key_id'],
        'aws_secret_access_key': config['secret_access_key'],
    }
