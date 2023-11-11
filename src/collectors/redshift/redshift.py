# coding=utf-8

"""
Collects data  about rds through  cloudwatch
#### Notes
  parameters :
  
   access_key_id: aws access key 
   secret_access_key:aws secret key
   DBInstanceIdentifiers: db name or * for all databases
  
  metrics will be published under rds.<dbname>.*
  
  **best practice is to use interval of every minute
  
  
  Dependencies

   botot
  """
from sqlite3 import Time
import boto
import datetime

from operator import itemgetter, attrgetter, methodcaller
import diamond.collector
import re

class RedshiftCollector(diamond.collector.Collector):

 def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(RedshiftCollector, self).get_default_config()
        config.update({
            'path': 'redshift',
        })
        return config


 def get_default_config_help(self):
        config_help = super(RedshiftCollector, self).get_default_config_help()
        config_help.update({
            'access_key_id': 'aws access_key',
            'secret_access_key': 'aws secret key',
            'ClusterIdentifiers': 'redshift cluster identifiers seperated by comma(db names)'
        })
        return config_help

 def collect(self):
    ClusterIdentifiers_arr=self.config['ClusterIdentifiers']
    cluster_attribs = ['CPUUtilization','DatabaseConnections','HealthStatus','MaintenanceMode','NetworkReceiveThroughput','NetworkTransmitThroughput','PercentageDiskSpaceUsed']
    node_attribs = ['CPUUtilization',
                   'NetworkReceiveThroughput',
                   'NetworkTransmitThroughput',
                   'PercentageDiskSpaceUsed',
                   'ReadIOPS',
                   'ReadLatency',
                   'ReadThroughput',
                   'WriteIOPS',
                   'WriteLatency',
                   'WriteThroughput']
    botoRDS = boto.connect_cloudwatch(aws_access_key_id=self.config['access_key_id'], aws_secret_access_key=self.config['secret_access_key'])
    redshift_connection=boto.connect_redshift(aws_access_key_id=self.config['access_key_id'], aws_secret_access_key=self.config['secret_access_key'])
    start_time=datetime.datetime.utcnow() - datetime.timedelta(seconds=120)
    end_time=datetime.datetime.utcnow()
    self.log.debug("checking  ClusterIdentifiers")
    self.log.debug(ClusterIdentifiers_arr)
    if ClusterIdentifiers_arr == '*':
        self.log.debug("getting all clusters")
        ClusterIdentifiers_arr=[]
        cluster_list_json=redshift_connection.describe_clusters()["DescribeClustersResponse"]["DescribeClustersResult"]["Clusters"]
        for clusters_json in cluster_list_json:
           ClusterIdentifiers_arr.append(clusters_json['ClusterIdentifier'])
    else :
        ClusterIdentifiers_arr=re.split(',',self.config['ClusterIdentifiers'])
    self.log.debug(ClusterIdentifiers_arr)
    for ClusterIdentifier in ClusterIdentifiers_arr:
        cluster_info=redshift_connection.describe_clusters(ClusterIdentifier)
        cluster_nodes=cluster_info["DescribeClustersResponse"]["DescribeClustersResult"]["Clusters"][0]["ClusterNodes"]
        for node in cluster_nodes:
            self.log.debug("getting data for node %s",node["NodeRole"])
            for attribute in node_attribs:
                self.log.debug("getting attribute %s",attribute)
                try:
                    lower=node["NodeRole"].lower()
                    instanceStats = botoRDS.get_metric_statistics(period=60,
                    start_time=start_time,
                    end_time=end_time,
                    namespace="AWS/Redshift",
                    metric_name=attribute,
                    statistics=["Sum"],
                    dimensions={'ClusterIdentifier':ClusterIdentifier ,'NodeID': lower.title()})
                    self.log.debug("instance state %s",instanceStats)
                except Exception,e:
                      self.log.error('An error occurred collecting from RedShift, %s', e)
                if instanceStats != []:
                   sorted_metric_arr=sorted(instanceStats, key=itemgetter('Timestamp'))
                   self.log.debug("publishing %s.%s.%s.%s" % (ClusterIdentifier,lower,attribute,  sorted_metric_arr[len(sorted_metric_arr)-1]['Sum']))
                   self.publish("%s.%s.%s" % (ClusterIdentifier,lower,attribute),  sorted_metric_arr[len(sorted_metric_arr)-1]['Sum'])
                   pass
        for attribute in cluster_attribs:
             try:
                instanceStats = botoRDS.get_metric_statistics(period=60,
                start_time=start_time,
                end_time=end_time,
                namespace="AWS/Redshift",
                metric_name=attribute,
                statistics=["Sum"],
                dimensions={'ClusterIdentifier':ClusterIdentifier})
             except Exception,e:
                  self.log.error('An error occurred collecting from RedShift, %s', e)
             if instanceStats != []:
               sorted_metric_arr=sorted(instanceStats, key=itemgetter('Timestamp'))
               self.publish("%s.%s" % (ClusterIdentifier + ".cluster",attribute) ,sorted_metric_arr[len(sorted_metric_arr)-1]['Sum'])
               pass