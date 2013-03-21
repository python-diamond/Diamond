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

    def _get(self, path):
        url = 'http://%s:%i/%s' % (
            self.config['host'], int(self.config['port']), path)
        try:
            response = urllib2.urlopen(url)
        except urllib2.HTTPError, err:
            self.log.error("%s: %s", url, err)
            return False

        try:
            return json.load(response)
        except (TypeError, ValueError):
            self.log.error("Unable to parse response from elasticsearch as a"
                           + " json object")
            return False

    def _index_metrics(self, metrics, prefix, index):
        metrics['%s.docs.count' % prefix] = index['docs']['count']
        metrics['%s.docs.deleted' % prefix] = index['docs']['deleted']
        metrics['%s.datastore.size' % prefix] = index['store']['size_in_bytes']

        # publish all 'total' and 'time_in_millis' stats
        for group, stats in index.iteritems():
            for key, value in stats.iteritems():
                if key.endswith('total') or key.endswith('time_in_millis'):
                    metrics['%s.%s.%s' % (prefix, group, key)] = value

    def collect(self):
        if json is None:
            self.log.error('Unable to import json')
            return {}

        result = self._get('_cluster/nodes/_local/stats?all=true')
        if not result:
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
        if 'field_evictions' in cache:
            metrics['cache.field.evictions'] = cache['field_evictions']
        if 'field_size_in_bytes' in cache:
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
        if 'fs' in data:
            fs_data = data['fs']['data'][0]
            metrics['disk.reads.count'] = fs_data['disk_reads']
            metrics['disk.reads.size'] = fs_data['disk_read_size_in_bytes']
            metrics['disk.writes.count'] = fs_data['disk_writes']
            metrics['disk.writes.size'] = fs_data['disk_write_size_in_bytes']

        #
        # individual index stats
        result = self._get('_stats?clear=true&docs=true&store=true&indexing=true&get=true&search=true')
        if not result:
            return

        _all = result['_all']
        self._index_metrics(metrics, 'indices._all', _all['primaries'])
        indices = _all['indices']
        for name, index in indices.iteritems():
            self._index_metrics(metrics, 'indices.%s' % name, index['primaries'])

        for key in metrics:
            self.publish(key, metrics[key])
