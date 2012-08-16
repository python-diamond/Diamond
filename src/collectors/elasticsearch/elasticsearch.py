# coding=utf-8

"""
Collect the elasticsearch stats for the local node

#### Dependencies

 * urlib2

"""

import json
import urllib2

import diamond.collector


class ElasticSearchCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(ElasticSearchCollector, self).get_default_config_help()
        config_help.update({
            'host' : "",
            'port' : "",
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(ElasticSearchCollector, self).get_default_config()
        config.update( {
            'host':     '127.0.0.1',
            'port':     9200,
            'path':     'elasticsearch',
        } )
        return config

    def collect(self):
        url = 'http://%s:%i/_cluster/nodes/_local/stats?all=true' % (
            self.config['host'], int(self.config['port']))
        try:
            response = urllib2.urlopen(url)
        except urllib2.HTTPError, err:
            self.log.error("%s: %s", url, err)
            return

        try:
            result = json.load(response)
        except (TypeError, ValueError):
            self.log.error("Unable to parse response from elasticsearch as a json object")
            return

        metrics = {}
        node = result['nodes'].keys()[0]
        data = result['nodes'][node]

        #
        # http connections to ES
        metrics['http.current'] = data['http']['current_open']

        #
        # indices
        metrics['indices.docs.count'] = data['indices']['docs']['count']
        metrics['indices.docs.deleted'] = data['indices']['docs']['deleted']

        metrics['indices.datastore.size'] = data['indices']['store']['size_in_bytes']

        #
        # process mem/cpu
        metrics['process.cpu.percent'] = data['process']['cpu']['percent']
        metrics['process.mem.resident'] = data['process']['mem']['resident_in_bytes']
        metrics['process.mem.share'] = data['process']['mem']['share_in_bytes']
        metrics['process.mem.virtual'] = data['process']['mem']['total_virtual_in_bytes']

        #
        # filesystem
        metrics['disk.reads.count'] = data['fs']['data'][0]['disk_reads']
        metrics['disk.reads.size'] = data['fs']['data'][0]['disk_read_size_in_bytes']
        metrics['disk.writes.count'] = data['fs']['data'][0]['disk_writes']
        metrics['disk.writes.size'] = data['fs']['data'][0]['disk_write_size_in_bytes']

        for key in metrics:
           self.publish(key, metrics[key])
