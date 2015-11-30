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

    PATHS = {
        'memory':
            "v2/metrics/mbean/java.lang:type=Memory",
        'queue':
            "v2/metrics/mbean/org.apache.activemq:BrokerName=localhost," +
            "Type=Queue,Destination=com.puppetlabs.puppetdb.commands",
        'processing-time':
            "v2/metrics/mbean/com.puppetlabs.puppetdb.command:" +
            "type=global,name=processing-time",
        'processed':
            "v2/metrics/mbean/com.puppetlabs.puppetdb.command:" +
            "type=global,name=processed",
        'retried':
            "v2/metrics/mbean/com.puppetlabs.puppetdb.command:" +
            "type=global,name=retried",
        'discarded':
            "v2/metrics/mbean/com.puppetlabs.puppetdb.command:" +
            "type=global,name=discarded",
        'fatal': "v2/metrics/mbean/com.puppetlabs.puppetdb.command:" +
                 "type=global,name=fatal",
        'commands.service-time':
            "v2/metrics/mbean/com.puppetlabs.puppetdb." +
            "http.server:type=/v3/commands,name=service-time",
        'resources.service-time':
            "v2/metrics/mbean/com.puppetlabs.puppetdb." +
            "http.server:type=/v3/resources,name=service-time",
        'gc-time':
            "v2/metrics/mbean/com.puppetlabs.puppetdb.scf.storage:" +
            "type=default,name=gc-time",
        'duplicate-pct':
            "v2/metrics/mbean/com.puppetlabs.puppetdb.scf.storage:" +
            "type=default,name=duplicate-pct",
        'pct-resource-dupes':
            "v2/metrics/mbean/com.puppetlabs.puppetdb.query." +
            "population:type=default,name=pct-resource-dupes",
        'num-nodes':
            "v2/metrics/mbean/com.puppetlabs.puppetdb.query." +
            "population:type=default,name=num-nodes",
        'num-resources':
            "v2/metrics/mbean/com.puppetlabs.puppetdb.query." +
            "population:type=default,name=num-resources",
    }

    def get_default_config_help(self):
        config_help = super(PuppetDBCollector,
                            self).get_default_config_help()
        config_help.update({
            'host': 'Hostname to collect from',
            'port': 'Port number to collect from',
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
        })
        return config

    def fetch_metrics(self, url):
        try:
            url = "http://%s:%s/%s" % (
                self.config['host'], int(self.config['port']), url)
            response = urllib2.urlopen(url)
        except Exception, e:
            self.log.error('Couldn\'t connect to puppetdb: %s -> %s', url, e)
            return {}
        return json.load(response)

    def collect(self):
        rawmetrics = {}
        for subnode in self.PATHS:
            path = self.PATHS[subnode]
            rawmetrics[subnode] = self.fetch_metrics(path)

        self.publish_gauge('num_resources',
                           rawmetrics['num-resources']['Value'])
        self.publish_gauge('catalog_duplicate_pct',
                           rawmetrics['duplicate-pct']['Value'])
        self.publish_gauge(
            'sec_command',
            time_convertor.convert(
                rawmetrics['processing-time']['50thPercentile'],
                rawmetrics['processing-time']['LatencyUnit'],
                'seconds'))
        self.publish_gauge(
            'resources_service_time',
            time_convertor.convert(
                rawmetrics['resources.service-time']['50thPercentile'],
                rawmetrics['resources.service-time']['LatencyUnit'],
                'seconds'))
        self.publish_gauge(
            'enqueueing_service_time',
            time_convertor.convert(
                rawmetrics['commands.service-time']['50thPercentile'],
                rawmetrics['commands.service-time']['LatencyUnit'],
                'seconds'))

        self.publish_gauge('discarded', rawmetrics['discarded']['Count'])
        self.publish_gauge('processed', rawmetrics['processed']['Count'])
        self.publish_gauge('rejected', rawmetrics['fatal']['Count'])
        self.publish_gauge(
            'DB_Compaction',
            time_convertor.convert(
                rawmetrics['gc-time']['50thPercentile'],
                rawmetrics['gc-time']['LatencyUnit'],
                'seconds'))
        self.publish_gauge('resource_duplicate_pct',
                           rawmetrics['pct-resource-dupes']['Value'])
        self.publish_gauge('num_nodes',
                           rawmetrics['num-nodes']['Value'])

        self.publish_counter('queue.ProducerCount',
                             rawmetrics['queue']['ProducerCount'])
        self.publish_counter('queue.DequeueCount',
                             rawmetrics['queue']['DequeueCount'])
        self.publish_counter('queue.ConsumerCount',
                             rawmetrics['queue']['ConsumerCount'])
        self.publish_gauge('queue.QueueSize',
                           rawmetrics['queue']['QueueSize'])
        self.publish_counter('queue.ExpiredCount',
                             rawmetrics['queue']['ExpiredCount'])
        self.publish_counter('queue.EnqueueCount',
                             rawmetrics['queue']['EnqueueCount'])
        self.publish_counter('queue.InFlightCount',
                             rawmetrics['queue']['InFlightCount'])
        self.publish_gauge('queue.CursorPercentUsage',
                           rawmetrics['queue']['CursorPercentUsage'])
        self.publish_gauge('queue.MemoryUsagePortion',
                           rawmetrics['queue']['MemoryUsagePortion'])

        self.publish_gauge('memory.NonHeapMemoryUsage.used',
                           rawmetrics['memory']['NonHeapMemoryUsage']['used'])
        self.publish_gauge(
            'memory.NonHeapMemoryUsage.committed',
            rawmetrics['memory']['NonHeapMemoryUsage']['committed'])
        self.publish_gauge('memory.HeapMemoryUsage.used',
                           rawmetrics['memory']['HeapMemoryUsage']['used'])
        self.publish_gauge('memory.HeapMemoryUsage.committed',
                           rawmetrics['memory']['HeapMemoryUsage']['committed'])
