# coding=utf-8

"""
Collect the DataStax OpsCenter metrics

#### Dependencies

 * urlib2

"""

import urllib2
import datetime

try:
    import json
except ImportError:
    import simplejson as json

import diamond.collector


class DseOpsCenterCollector(diamond.collector.Collector):
    last_run_time = 0
    column_families = None
    last_schema_sync_time = 0

    def get_default_config_help(self):
        config_help = super(DseOpsCenterCollector,
                            self).get_default_config_help()
        config_help.update({
            'host': "",
            'port': "",
            'cluster_id': "Set cluster ID/name.\n",
            'metrics': "You can list explicit metrics if you like,\n"
            " by default all know metrics are included.\n",
            'node_group': "Set node group name, any by default\n",
            'default_tail_opts': "Chaning these is not recommended.",
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(DseOpsCenterCollector, self).get_default_config()
        metrics = [
            'cf-bf-false-positives',
            'cf-bf-false-ratio',
            'cf-bf-space-used',
            'cf-keycache-hit-rate',
            'cf-keycache-hits',
            'cf-keycache-requests',
            'cf-live-disk-used',
            'cf-live-sstables',
            'cf-pending-tasks',
            'cf-read-latency-op',
            'cf-read-ops',
            'cf-rowcache-hit-rate',
            'cf-rowcache-hits',
            'cf-rowcache-requests',
            'cf-total-disk-used',
            'cf-write-latency-op',
            'cf-write-ops',
            'cms-collection-count',
            'cms-collection-time',
            'data-load',
            'heap-committed',
            'heap-max',
            'heap-used',
            'key-cache-hit-rate',
            'key-cache-hits',
            'key-cache-requests',
            'nonheap-committed',
            'nonheap-max',
            'nonheap-used',
            'pending-compaction-tasks',
            'pending-flush-sorter-tasks',
            'pending-flushes',
            'pending-gossip-tasks',
            'pending-hinted-handoff',
            'pending-internal-responses',
            'pending-memtable-post-flushers',
            'pending-migrations',
            'pending-misc-tasks',
            'pending-read-ops',
            'pending-read-repair-tasks',
            'pending-repair-tasks',
            'pending-repl-on-write-tasks',
            'pending-request-responses',
            'pending-streams',
            'pending-write-ops',
            'read-latency-op',
            'read-ops',
            'row-cache-hit-rate',
            'row-cache-hits',
            'row-cache-requests',
            'solr-avg-time-per-req',
            'solr-errors',
            'solr-requests',
            'solr-timeouts',
            'total-bytes-compacted',
            'total-compactions-completed',
            'write-latency-op',
            'write-ops',
        ]
        config.update({
            'host':              '127.0.0.1',
            'port':              8888,
            'path':              'cassandra',
            'node_group':        '*',
            'metrics':           ','.join(metrics),
            'default_tail_opts': '&forecast=0&node_aggregation=1',

        })
        return config

    def _get_schema(self):
        time_now = int(datetime.datetime.utcnow().strftime('%s'))
        if (self.column_families is None
                or (time_now - self.last_schema_sync_time < 3600)):
            return False
        url = 'http://%s:%i/%s/keyspaces' % (self.config['host'],
                                             int(self.config['port']),
                                             self.config['cluster_id'])
        try:
            response = urllib2.urlopen(url)
        except Exception, err:
            self.log.error('%s: %s', url, err)
            return False

        try:
            result = json.load(response)
            column_families = []
            for ks in result:
                i = []
                for cf in result[ks]['column_families']:
                    i.append("%s.%s" % (ks, cf))
                column_families.append(i)
            self.column_families = ','.join(sum(column_families, []))
            self.log.debug('DseOpsCenterCollector columnfamilies = %s',
                           self.column_families)
            self.last_schema_sync_time = time_now
            return True

        except (TypeError, ValueError):
            self.log.error(
                "Unable to parse response from opscenter as a json object")
            return False

    def _get(self, start, end, step=60):
        self._get_schema()
        url = ('http://%s:%i/%s/new-metrics?node_group=%s&columnfamilies=%s'
               '&metrics=%s&start=%i&end=%i&step=%i%s') % (
            self.config['host'],
            int(self.config['port']),
            self.config['cluster_id'],
            self.config['node_group'],
            self.column_families,
            self.config['metrics'],
            start, end, step,
            self.config['default_tail_opts'])

        try:
            response = urllib2.urlopen(url)
        except Exception, err:
            self.log.error('%s: %s', url, err)
            return False

        self.log.debug('DseOpsCenterCollector metrics url = %s', url)

        try:
            return json.load(response)
        except (TypeError, ValueError):
            self.log.error(
                "Unable to parse response from opscenter as a json object")
            return False

    def collect(self):
        metrics = {}
        if json is None:
            self.log.error('Unable to import json')
            return None

        time_now = int(datetime.datetime.utcnow().strftime('%s'))

        self.log.debug('DseOpsCenterCollector last_run_time = %i',
                       self.last_run_time)

        if self.last_run_time == 0:
            self.last_run_time = time_now - 60
        if time_now - self.last_run_time >= 60:
            result = self._get(self.last_run_time, time_now)
            self.last_run_time = time_now
            if not result:
                return None
            self.log.debug('DseOpsCenterCollector result = %s', result)
            for data in result['data'][self.config['node_group']]:
                if data['data-points'][0][0] is None:
                    if 'columnfamily' in data:
                        k = '.'.join([data['metric'],
                                      data['columnfamily']])
                        metrics[k] = data['data-points'][0][0]
                else:
                    metrics[data['metric']] = data['data-points'][0][0]
            self.log.debug('DseOpsCenterCollector metrics = %s', metrics)
            for key in metrics:
                self.publish(key, metrics[key])
        else:
            self.log.debug(
                "DseOpsCenterCollector can only run once every minute")
            return None
