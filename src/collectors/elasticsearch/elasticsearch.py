# coding=utf-8

"""
Collect the elasticsearch stats for the local node

#### Dependencies

 * urlib2

"""

import urllib2

try:
    import json
    json  # workaround for pyflakes issue #13
except ImportError:
    import simplejson as json

import diamond.collector


class ElasticSearchCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(ElasticSearchCollector,
                            self).get_default_config_help()
        config_help.update({
            'host': "",
            'port': "",
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(ElasticSearchCollector, self).get_default_config()
        config.update({
            'host':     '127.0.0.1',
            'port':     9200,
            'path':     'elasticsearch',
        })
        return config

    def collect(self):
        if json is None:
            self.log.error('Unable to import json')
            return {}
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
            self.log.error("Unable to parse response from elasticsearch as a"
                           + " json object")
            return

        metrics = {}
        node = result['nodes'].keys()[0]
        data = result['nodes'][node]

        #
        # http connections to ES
        metrics['http.current'] = data['http']['current_open']

        #
        # indices
        indices = data['indices']
        metrics['indices.docs.count'] = indices['docs']['count']
        metrics['indices.docs.deleted'] = indices['docs']['deleted']

        metrics['indices.datastore.size'] = indices['store']['size_in_bytes']

        transport = data['transport']
        metrics['transport.rx.count'] = transport['rx_count']
        metrics['transport.rx.size'] = transport['rx_size_in_bytes']
        metrics['transport.tx.count'] = transport['tx_count']
        metrics['transport.tx.size'] = transport['tx_size_in_bytes']

        cache = indices['cache']
        if 'bloom_size_in_bytes' in cache:
            metrics['cache.bloom.size'] = cache['bloom_size_in_bytes']
        metrics['cache.field.evictions'] = cache['field_evictions']
        metrics['cache.field.size'] = cache['field_size_in_bytes']
        metrics['cache.filter.count'] = cache['filter_count']
        metrics['cache.filter.evictions'] = cache['filter_evictions']
        metrics['cache.filter.size'] = cache['filter_size_in_bytes']
        if 'id_cache_size_in_bytes' in cache:
            metrics['cache.id.size'] = cache['id_cache_size_in_bytes']

        #
        # process mem/cpu
        process = data['process']
        mem = process['mem']
        metrics['process.cpu.percent'] = process['cpu']['percent']
        metrics['process.mem.resident'] = mem['resident_in_bytes']
        metrics['process.mem.share'] = mem['share_in_bytes']
        metrics['process.mem.virtual'] = mem['total_virtual_in_bytes']

        #
        # filesystem
        fs_data = data['fs']['data'][0]
        metrics['disk.reads.count'] = fs_data['disk_reads']
        metrics['disk.reads.size'] = fs_data['disk_read_size_in_bytes']
        metrics['disk.writes.count'] = fs_data['disk_writes']
        metrics['disk.writes.size'] = fs_data['disk_write_size_in_bytes']

        for key in metrics:
            self.publish(key, metrics[key])
