# coding=utf-8

"""
Collect the elasticsearch stats for the local node.

Supports multiple instances. When using the 'instances'
parameter the instance alias will be appended to the
'path' parameter.

#### Dependencies

 * urlib2

"""

import urllib2
import base64
import re
from diamond.collector import str_to_bool

try:
    import json
except ImportError:
    import simplejson as json

import diamond.collector

RE_LOGSTASH_INDEX = re.compile('^(.*)-\d{4}(\.\d{2}){2,3}$')


class ElasticSearchCollector(diamond.collector.Collector):

    def process_config(self):
        super(ElasticSearchCollector, self).process_config()
        instance_list = self.config['instances']
        if isinstance(instance_list, basestring):
            instance_list = [instance_list]

        if len(instance_list) == 0:
            host = self.config['host']
            port = self.config['port']
            # use empty alias to identify single-instance config
            # omitting the use of the alias in the metrics path
            instance_list.append('@%s:%s' % (host, port))

        self.instances = {}
        for instance in instance_list:
            if '@' in instance:
                (alias, hostport) = instance.split('@', 1)
            else:
                alias = 'default'
                hostport = instance

            if ':' in hostport:
                host, port = hostport.split(':', 1)
            else:
                host = hostport
                port = 9200

            self.instances[alias] = (host, int(port))

    def get_default_config_help(self):
        config_help = super(ElasticSearchCollector,
                            self).get_default_config_help()
        config_help.update({
            'host': "",
            'port': "",
            'user': "Username for Basic/Shield auth",
            'password': "Password for Basic/Shield auth",
            'instances': "List of instances. When set this overrides "
            "the 'host' and 'port' settings. Instance format: "
            "instance [<alias>@]<hostname>[:<port>]",
            'scheme': "http (default) or https",
            'cluster': "cluster/node/shard health",
            'stats':
                "Available stats:\n" +
                " - jvm (JVM information)\n" +
                " - thread_pool (Thread pool information)\n" +
                " - indices (Individual index stats)\n",
            'logstash_mode':
                "If 'indices' stats are gathered, remove " +
                "the YYYY.MM.DD suffix from the index name " +
                "(e.g. logstash-adm-syslog-2014.01.03) and use that " +
                "as a bucket for all 'day' index stats.",
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(ElasticSearchCollector, self).get_default_config()
        config.update({
            'host':           '127.0.0.1',
            'port':           9200,
            'user':           '',
            'password':       '',
            'instances':      [],
            'scheme':         'http',
            'path':           'elasticsearch',
            'stats':          ['jvm', 'thread_pool', 'indices'],
            'logstash_mode': False,
            'cluster':       False,
        })
        return config

    def _get(self, scheme, host, port, path, assert_key=None):
        """
        Execute a ES API call. Convert response into JSON and
        optionally assert its structure.
        """
        url = '%s://%s:%i/%s' % (scheme, host, port, path)
        try:
            request = urllib2.Request(url)
            if self.config['user'] and self.config['password']:
                base64string = base64.standard_b64encode(
                    '%s:%s' % (self.config['user'], self.config['password']))
                request.add_header("Authorization", "Basic %s" % base64string)
            response = urllib2.urlopen(request)
        except Exception as err:
            self.log.error("%s: %s" % (url, err))
            return False

        try:
            doc = json.load(response)
        except (TypeError, ValueError):
            self.log.error("Unable to parse response from elasticsearch as a" +
                           " json object")
            return False

        if assert_key and assert_key not in doc:
            self.log.error("Bad response from elasticsearch, expected key "
                           "'%s' was missing for %s" % (assert_key, url))
            return False
        return doc

    def _copy_one_level(self, metrics, prefix, data, filter=lambda key: True):
        for key, value in data.iteritems():
            if filter(key):
                metric_path = '%s.%s' % (prefix, key)
                self._set_or_sum_metric(metrics, metric_path, value)

    def _copy_two_level(self, metrics, prefix, data, filter=lambda key: True):
        for key1, d1 in data.iteritems():
            self._copy_one_level(metrics, '%s.%s' % (prefix, key1), d1, filter)

    def _index_metrics(self, metrics, prefix, index):
        if self.config['logstash_mode']:
            """Remove the YYYY.MM.DD bit from logstash indices.
            This way we keep using the same metric naming and not polute
            our metrics system (e.g. Graphite) with new metrics every day."""
            m = RE_LOGSTASH_INDEX.match(prefix)
            if m:
                prefix = m.group(1)

                # keep a telly of the number of indexes
                self._set_or_sum_metric(metrics,
                                        '%s.indexes_in_group' % prefix, 1)

        self._add_metric(metrics, '%s.docs.count' % prefix, index,
                         ['docs', 'count'])
        self._add_metric(metrics, '%s.docs.deleted' % prefix, index,
                         ['docs', 'deleted'])
        self._add_metric(metrics, '%s.datastore.size' % prefix, index,
                         ['store', 'size_in_bytes'])

        # publish all 'total' and 'time_in_millis' stats
        self._copy_two_level(
            metrics, prefix, index,
            lambda key: key.endswith('total') or key.endswith('time_in_millis') or key.endswith('in_bytes'))  # noqa

    def _add_metric(self, metrics, metric_path, data, data_path):
        """If the path specified by data_path (a list) exists in data,
        add to metrics.  Use when the data path may not be present"""
        current_item = data
        for path_element in data_path:
            current_item = current_item.get(path_element)
            if current_item is None:
                return

        self._set_or_sum_metric(metrics, metric_path, current_item)

    def _set_or_sum_metric(self, metrics, metric_path, value):
        """If we already have a datapoint for this metric, lets add
        the value. This is used when the logstash mode is enabled."""
        if metric_path in metrics:
            metrics[metric_path] += value
        else:
            metrics[metric_path] = value

    def collect_instance_cluster_stats(self, scheme, host, port, metrics):
        result = self._get(scheme, host, port, '_cluster/health')
        if not result:
            return

        self._add_metric(metrics, 'cluster_health.nodes.total',
                         result, ['number_of_nodes'])
        self._add_metric(metrics, 'cluster_health.nodes.data',
                         result, ['number_of_data_nodes'])
        self._add_metric(metrics, 'cluster_health.nodes.pending_tasks',
                         result, ['number_of_pending_tasks'])
        self._add_metric(metrics, 'cluster_health.shards.active_primary',
                         result, ['active_primary_shards'])
        self._add_metric(metrics, 'cluster_health.shards.active',
                         result, ['active_shards'])
        self._add_metric(metrics, 'cluster_health.shards.active_percent',
                         result, ['active_shards_percent_as_number'])
        self._add_metric(metrics, 'cluster_health.shards.delayed_unassigned',
                         result, ['delayed_unassigned_shards'])
        self._add_metric(metrics, 'cluster_health.shards.relocating',
                         result, ['relocating_shards'])
        self._add_metric(metrics, 'cluster_health.shards.unassigned',
                         result, ['unassigned_shards'])
        self._add_metric(metrics, 'cluster_health.shards.initializing',
                         result, ['initializing_shards'])

        CLUSTER_STATUS = {
            'green': 2,
            'yellow': 1,
            'red': 0
        }
        metrics['cluster_health.status'] = CLUSTER_STATUS[result['status']]

    def collect_instance_index_stats(self, scheme, host, port, metrics):
        result = self._get(scheme, host, port, '_stats', '_all')
        if not result:
            return

        _all = result['_all']
        self._index_metrics(metrics, 'indices._all', _all['primaries'])

        if 'indices' in _all:
            indices = _all['indices']
        elif 'indices' in result:          # elasticsearch >= 0.90RC2
            indices = result['indices']
        else:
            return

        for name, index in indices.iteritems():
            self._index_metrics(metrics, 'indices.%s' % name,
                                index['primaries'])

    def collect_instance(self, alias, scheme, host, port):
        result = self._get(scheme, host, port, '_nodes/_local/stats', 'nodes')
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

        # elasticsearch < 0.90RC2
        if 'cache' in indices:
            cache = indices['cache']

            self._add_metric(metrics, 'cache.bloom.size', cache,
                             ['bloom_size_in_bytes'])
            self._add_metric(metrics, 'cache.field.evictions', cache,
                             ['field_evictions'])
            self._add_metric(metrics, 'cache.field.size', cache,
                             ['field_size_in_bytes'])
            metrics['cache.filter.count'] = cache['filter_count']
            metrics['cache.filter.evictions'] = cache['filter_evictions']
            metrics['cache.filter.size'] = cache['filter_size_in_bytes']
            self._add_metric(metrics, 'cache.id.size', cache,
                             ['id_cache_size_in_bytes'])

        # elasticsearch >= 0.90RC2
        if 'filter_cache' in indices:
            cache = indices['filter_cache']

            metrics['cache.filter.evictions'] = cache['evictions']
            metrics['cache.filter.size'] = cache['memory_size_in_bytes']
            self._add_metric(metrics, 'cache.filter.count', cache, ['count'])

        # elasticsearch >= 0.90RC2
        if 'id_cache' in indices:
            cache = indices['id_cache']

            self._add_metric(metrics, 'cache.id.size', cache,
                             ['memory_size_in_bytes'])

        if 'query_cache' in indices:
            cache = indices['query_cache']

            metrics['cache.query.evictions'] = cache['evictions']
            metrics['cache.query.size'] = cache['memory_size_in_bytes']
            self._add_metric(metrics, 'cache.query.hit_count', cache,
                             ['hit_count'])
            self._add_metric(metrics, 'cache.query.miss_count', cache,
                             ['miss_count'])

        # elasticsearch >= 0.90
        if 'fielddata' in indices:
            fielddata = indices['fielddata']
            self._add_metric(metrics, 'fielddata.size', fielddata,
                             ['memory_size_in_bytes'])
            self._add_metric(metrics, 'fielddata.evictions', fielddata,
                             ['evictions'])

        if 'segments' in indices:
            segments = indices['segments']
            self._add_metric(metrics, 'segments.count', segments, ['count'])
            self._add_metric(metrics, 'segments.mem.size', segments,
                             ['memory_in_bytes'])
            self._add_metric(metrics, 'segments.index_writer.mem.size',
                             segments, ['index_writer_memory_in_bytes'])
            self._add_metric(metrics, 'segments.index_writer.mem.max_size',
                             segments, ['index_writer_max_memory_in_bytes'])
            self._add_metric(metrics, 'segments.version_map.mem.size',
                             segments, ['version_map_memory_in_bytes'])
            self._add_metric(metrics, 'segments.fixed_bit_set.mem.size',
                             segments, ['fixed_bit_set_memory_in_bytes'])

        #
        # process mem/cpu (may not be present, depending on access
        # restrictions)
        self._add_metric(metrics, 'process.cpu.percent', data,
                         ['process', 'cpu', 'percent'])
        self._add_metric(metrics, 'process.mem.resident', data,
                         ['process', 'mem', 'resident_in_bytes'])
        self._add_metric(metrics, 'process.mem.share', data,
                         ['process', 'mem', 'share_in_bytes'])
        self._add_metric(metrics, 'process.mem.virtual', data,
                         ['process', 'mem', 'total_virtual_in_bytes'])

        #
        # filesystem (may not be present, depending on access restrictions)
        if 'fs' in data and 'data' in data['fs'] and data['fs']['data']:
            fs_data = data['fs']['data'][0]
            self._add_metric(metrics, 'disk.reads.count', fs_data,
                             ['disk_reads'])
            self._add_metric(metrics, 'disk.reads.size', fs_data,
                             ['disk_read_size_in_bytes'])
            self._add_metric(metrics, 'disk.writes.count', fs_data,
                             ['disk_writes'])
            self._add_metric(metrics, 'disk.writes.size', fs_data,
                             ['disk_write_size_in_bytes'])

        #
        # jvm
        if 'jvm' in self.config['stats']:
            jvm = data['jvm']
            mem = jvm['mem']
            for k in ('heap_used', 'heap_committed', 'non_heap_used',
                      'non_heap_committed'):
                metrics['jvm.mem.%s' % k] = mem['%s_in_bytes' % k]

            if 'heap_used_percent' in mem:
                metrics['jvm.mem.heap_used_percent'] = mem['heap_used_percent']

            for pool, d in mem['pools'].iteritems():
                pool = pool.replace(' ', '_')
                metrics['jvm.mem.pools.%s.used' % pool] = d['used_in_bytes']
                metrics['jvm.mem.pools.%s.max' % pool] = d['max_in_bytes']

            metrics['jvm.threads.count'] = jvm['threads']['count']

            gc = jvm['gc']
            collection_count = 0
            collection_time_in_millis = 0
            for collector, d in gc['collectors'].iteritems():
                metrics['jvm.gc.collection.%s.count' % collector] = d[
                    'collection_count']
                collection_count += d['collection_count']
                metrics['jvm.gc.collection.%s.time' % collector] = d[
                    'collection_time_in_millis']
                collection_time_in_millis += d['collection_time_in_millis']
            # calculate the totals, as they're absent in elasticsearch >
            # 0.90.10
            if 'collection_count' in gc:
                metrics['jvm.gc.collection.count'] = gc['collection_count']
            else:
                metrics['jvm.gc.collection.count'] = collection_count

            k = 'collection_time_in_millis'
            if k in gc:
                metrics['jvm.gc.collection.time'] = gc[k]
            else:
                metrics['jvm.gc.collection.time'] = collection_time_in_millis

        #
        # thread_pool
        if 'thread_pool' in self.config['stats']:
            self._copy_two_level(metrics, 'thread_pool', data['thread_pool'])

        #
        # network
        if 'network' in data:
            self._copy_two_level(metrics, 'network', data['network'])

        #
        # cluster (optional)
        if str_to_bool(self.config['cluster']):
            self.collect_instance_cluster_stats(scheme, host, port, metrics)

        #
        # indices (optional)
        if 'indices' in self.config['stats']:
            self.collect_instance_index_stats(scheme, host, port, metrics)

        #
        # all done, now publishing all metrics
        for key in metrics:
            full_key = key
            if alias != '':
                full_key = '%s.%s' % (alias, full_key)
            self.publish(full_key, metrics[key])

    def collect(self):
        if json is None:
            self.log.error('Unable to import json')
            return {}

        scheme = self.config['scheme']
        for alias in sorted(self.instances):
            (host, port) = self.instances[alias]
            self.collect_instance(alias, scheme, host, port)
