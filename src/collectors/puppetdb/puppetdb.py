# coding=utf-8

"""
Collect metrics from Puppet DB Dashboard

#### Dependencies

 * urllib2
 * json

"""

import urllib2
import diamond.collector
from diamond.convertor import time as time_convertor

try:
    import json
except ImportError:
    import simplejson as json


class PuppetDBCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(PuppetDBCollector,
                            self).get_default_config_help()
        config_help.update({
            'host': 'Hostname to collect from',
            'port': 'Port number to collect from',
            'metric_path': 'metrics/v1/mbeans',
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(PuppetDBCollector, self).get_default_config()
        config.update({
            'host': 'localhost',
            'port': 8080,
            'path': 'PuppetDB',
            'metric_path': 'metrics/v1/mbeans',
        })
        return config

    def metrics_name(self, path):
        try:
            response = {}
            for key, value in path.iteritems():
                if type(value) is int or type(value) is float:
                    response[key] = value
        except Exception, e:
            self.log.error('Couldn\'t parse the given value %s', path, e)
            return {}
        return response

    def fetch_metrics(self, url):
        try:
            url = "http://%s:%s/%s/%s" % (
                self.config['host'], int(self.config['port']),
                self.config['metric_path'], url)
            response = urllib2.urlopen(url)
        except Exception, e:
            self.log.error('Couldn\'t connect to puppetdb: %s -> %s', url, e)
            return {}
        return json.load(response)

    def send_data(self, metric_name, metric):
        try:
            if metric is not None:
                for key, value in self.metrics_name(metric).iteritems():
                    self.publish_gauge('%s.%s' % (metric_name, key), value)
        except Exception, e:
            self.log.error('Couldn\'t send metrics for this %s', metric, e)

    def collect(self):
        if 'v1' in self.config['metric_path']:
            PATHS = {
                'memory':
                    "java.lang:type=Memory",
                'queue':
                    "org.apache.activemq:type=Broker,brokerName=localhost," +
                    "destinationType=Queue,destinationName=" +
                    "puppetlabs.puppetdb.commands",
                'processing-time':
                    "puppetlabs.puppetdb.mq:name=global.processing-time",
                'processed':
                    "puppetlabs.puppetdb.mq:name=global.processed",
                'retried':
                    "puppetlabs.puppetdb.mq:name=global.retried",
                'discarded':
                    "puppetlabs.puppetdb.mq:name=global.discarded",
                'fatal':
                    "puppetlabs.puppetdb.mq:name=global.fatal",
                'commands.service-time':
                    "puppetlabs.puppetdb.http:name=/pdb/cmd/v1.service-time",
                'resources.service-time':
                    "puppetlabs.puppetdb.http:name=" +
                    "/pdb/query/v4/resources.service-time",
                'gc-time':
                    "puppetlabs.puppetdb.storage:name=gc-time",
                'duplicate-pct':
                    "puppetlabs.puppetdb.storage:name=duplicate-pct",
                'pct-resource-dupes':
                    "puppetlabs.puppetdb.population:name=pct-resource-dupes",
                'num-nodes':
                    "puppetlabs.puppetdb.population:name=num-nodes",
                'num-resources':
                    "puppetlabs.puppetdb.population:name=num-resources",
                'resources-per-node':
                    "puppetlabs.puppetdb.population:name=" +
                    "avg-resources-per-node",
            }
        else:
            PATHS = {
                'memory':
                    "java.lang:type=Memory",
                'queue':
                    "org.apache.activemq:BrokerName=localhost,Type=Queue," +
                    "Destination=com.puppetlabs.puppetdb.commands",
                'processing-time':
                    "com.puppetlabs.puppetdb.command:type=" +
                    "global,name=processing-time",
                'processed':
                    "com.puppetlabs.puppetdb.command:type=" +
                    "global,name=processed",
                'retried':
                    "com.puppetlabs.puppetdb.command:type=" +
                    "global,name=retried",
                'discarded':
                    "com.puppetlabs.puppetdb.command:type=" +
                    "global,name=discarded",
                'fatal':
                    "com.puppetlabs.puppetdb.command:type=global,name=fatal",
                'commands.service-time':
                    "com.puppetlabs.puppetdb.http.server:" +
                    "type=/v3/commands,name=service-time",
                'resources.service-time':
                    "com.puppetlabs.puppetdb.http.server:" +
                    "type=/v3/resources,name=service-time",
                'gc-time':
                    "com.puppetlabs.puppetdb.scf.storage:" +
                    "type=default,name=gc-time",
                'duplicate-pct':
                    "com.puppetlabs.puppetdb.scf.storage:" +
                    "type=default,name=duplicate-pct",
                'pct-resource-dupes':
                    "com.puppetlabs.puppetdb.query.population" +
                    ":type=default,name=pct-resource-dupes",
                'num-nodes':
                    "com.puppetlabs.puppetdb.query.population" +
                    ":type=default,name=num-nodes",
                'num-resources':
                    "com.puppetlabs.puppetdb.query.population" +
                    ":type=default,name=num-resources",
            }

        rawmetrics = {}

        for subnode in PATHS:
            path = PATHS[subnode]
            rawmetrics[subnode] = self.fetch_metrics(path)

        # Memory
        # NonHeapMemoryUsage
        memory = ['NonHeapMemoryUsage', 'HeapMemoryUsage']
        values = ['committed', 'init', 'max', 'used']
        for i in memory:
            for v in values:
                self.publish_gauge(
                    'memory.%s.%s' % (i, v),
                    rawmetrics['memory'][i][v]
                )

        # Send Data
        self.send_data('queue', rawmetrics['queue'])
        self.send_data('processing_time', rawmetrics['processing-time'])
        self.send_data('processed', rawmetrics['processed'])
        self.send_data('retried', rawmetrics['retried'])
        self.send_data('discarded', rawmetrics['discarded'])
        self.send_data('fatal', rawmetrics['fatal'])
        self.send_data(
            'commands.service-time',
            rawmetrics['commands.service-time']
        )
        self.send_data(
            'resources.service-time',
            rawmetrics['resources.service-time']
        )
        self.send_data('gc-time', rawmetrics['gc-time'])
        self.send_data('duplicate-pct', rawmetrics['duplicate-pct'])
        self.send_data('pct-resource-dupes', rawmetrics['pct-resource-dupes'])
        self.send_data('num-nodes', rawmetrics['num-nodes'])
        self.send_data('num-resources', rawmetrics['num-resources'])
        self.send_data('resources-per-node', rawmetrics['resources-per-node'])
