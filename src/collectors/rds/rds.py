# coding=utf-8

"""
Collects data from  rds through  cloudwatch
#### Notes
  parameters :
  
   access_key_id: aws access key 
   secret_access_key:aws secret key
   DBInstanceIdentifiers: db name
  
  metrics will be published under rds.<dbname>.*
  
  **best practice is to use interval of every minute
  
  
  Dependencies

   boto
  """


from sqlite3 import Time
import boto
import datetime

from operator import itemgetter, attrgetter, methodcaller
import diamond.collector
import re

class RdsCollector(diamond.collector.Collector):

 def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(RdsCollector, self).get_default_config()
        config.update({
            'access_key_id': 'access_key',
            'secret_access_key': 'secret_key',
            'DBInstanceIdentifiers': 'test'
        })
        return config


 def get_default_config_help(self):
        config_help = super(RdsCollector, self).get_default_config_help()
        config_help.update({
            'access_key_id': 'aws access key',
            'secret_access_key': 'aws secret key',
            'DBInstanceIdentifiers': 'enter queues seperated by comma'
        })
        return config_help

 def collect(self):
    DBInstanceIdentifiers_arr=re.split(',',self.config['DBInstanceIdentifiers'])
    instanceStats = []
    attribs = ['BinLogDiskUsage',
                   'CPUUtilization',
                   'DatabaseConnections',
                   'DiskQueueDepth',
                   'FreeableMemory',
                   'FreeStorageSpace',
                   'ReplicaLag',
                   'SwapUsage',
                   'ReadIOPS',
                   'WriteIOPS',
                   'ReadLatency',
                   'WriteLatency',
                   'ReadThroughput',
                   'WriteThroughput',
                   'NetworkReceiveThroughput',
                   'NetworkTransmitThroughput']
    botoRDS = boto.connect_cloudwatch(aws_access_key_id=self.config['access_key_id'], aws_secret_access_key=self.config['secret_access_key'])
    for dbInstanceIdentifier in DBInstanceIdentifiers_arr:
        for attribute in attribs:
            try:
                instanceStats = botoRDS.get_metric_statistics(period=60,
                start_time=datetime.datetime.utcnow() - datetime.timedelta(seconds=120),
                end_time=datetime.datetime.utcnow(),
                namespace="AWS/RDS",
                metric_name=attribute,
                statistics=["Sum"],
                dimensions={'DBInstanceIdentifier':dbInstanceIdentifier})
            except Exception:
                self.log.error('An error occurred collecting from RDS, %s', e)
            if instanceStats != []:
               sorted_metric_arr=sorted(instanceStats, key=itemgetter('Timestamp'))
               self.publish('%s.%s' % (dbInstanceIdentifier,attribute),sorted_metric_arr[len(sorted_metric_arr)-1]['Sum'])