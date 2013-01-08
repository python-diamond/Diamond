# coding=utf-8

"""
The S3BucketCollector collects bucket size using boto

#### Dependencies

  * boto (https://github.com/boto/boto)
"""

import diamond.collector
try:
    import boto
    boto
    from boto.s3.connection import S3Connection
except ImportError:
    boto = None


class S3BucketCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(S3BucketCollector, self).get_default_config_help()
        config_help.update({
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(S3BucketCollector, self).get_default_config()
        config.update({
            'enabled':   'False',
            'path':      'aws.s3',
            'byte_unit': 'byte'
        })
        return config

    def getBucket(self, aws_access, aws_secret, bucket_name):
        self.log.info("S3: Open Bucket, %s, %s, %s" % (bucket_name, aws_access,
                                                       aws_secret))
        s3 = S3Connection(aws_access, aws_secret)
        return s3.lookup(bucket_name)

    def getBucketSize(self, bucket):
        total_bytes = 0
        for key in bucket:
            total_bytes += key.size
        return total_bytes

    def collect(self):
        """
        Collect s3 bucket stats
        """
        if boto is None:
            self.log.error("Unable to import boto python module")
            return {}
        for s3instance in self.config['s3']:
            self.log.info("S3: byte_unit: %s" % self.config['byte_unit'])
            aws_access = self.config['s3'][s3instance]['aws_access_key']
            aws_secret = self.config['s3'][s3instance]['aws_secret_key']
            for bucket_name in self.config['s3'][s3instance]['buckets']:
                bucket = self.getBucket(aws_access, aws_secret, bucket_name)

                # collect bucket size
                total_size = self.getBucketSize(bucket)
                for byte_unit in self.config['byte_unit']:
                    new_size = diamond.convertor.binary.convert(
                        value=total_size,
                        oldUnit='byte',
                        newUnit=byte_unit
                    )
                    self.publish("%s.size.%s" % (bucket_name, byte_unit,
                                                 new_size))
