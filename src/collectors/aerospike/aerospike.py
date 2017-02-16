# coding=utf-8

"""
Collect statistics from Aerospike

#### Dependencies

 * socket
 * telnetlib
 * re


"""
import socket
import telnetlib
import re
import diamond.collector


class AerospikeCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(AerospikeCollector, self).get_default_config_help()
        config_help.update({
            'req_host': 'Hostname',
            'req_port': 'Port',
            'statistics': 'Collect statistics',
            'latency': 'Collect latency metrics',
            'throughput': 'Collect throughput metrics',
            'namespaces': 'Collect per-namespace metrics',
            'namespaces_whitelist':
                'List of namespaces to collect metrics' +
                ' from (default is to collect from all)',
            'statistics_whitelist':
                'List of global statistics values to collect',
            'namespace_statistics_whitelist':
                'List of per-namespace statistics values to collect',
            'path': 'Metric path',

        })
        return config_help

    def get_default_config(self):
        default_config = super(AerospikeCollector, self).get_default_config()
        default_config['req_host'] = 'localhost'
        default_config['req_port'] = 3003
        default_config['statistics'] = True
        default_config['latency'] = True
        default_config['throughput'] = True
        default_config['namespaces'] = True
        default_config['namespaces_whitelist'] = False
        default_config['statistics_whitelist'] = [
            'total-bytes-memory',
            'total-bytes-disk',
            'used-bytes-memory',
            'used-bytes-disk',
            'free-pct-memory',
            'free-pct-disk',
            'data-used-bytes-memory',
            'cluster_size',
            'objects',
            'client_connections',
            'index-used-bytes-memory',
        ]
        default_config['namespace_statistics_whitelist'] = [
            'objects',
            'evicted-objects',
            'expired-objects',
            'used-bytes-memory',
            'data-used-bytes-memory',
            'index-used-bytes-memory',
            'used-bytes-disk',
            'memory-size',
            'total-bytes-memory',
            'total-bytes-disk',
            'migrate-tx-partitions-initial',
            'migrate-tx-partitions-remaining',
            'migrate-rx-partitions-initial',
            'migrate-rx-partitions-remaining',
            'available_pct',
        ]
        default_config['path'] = 'aerospike'

        return default_config

    def collect_latency(self, data):

        # Get individual data lines (every other output line is data)
        raw_lines = {}
        (
            raw_lines['reads'],
            raw_lines['writes_master'],
            raw_lines['proxy'],
            raw_lines['udf'],
            raw_lines['query'],
        ) = data.split(';')[1::2]

        # Collapse each type of data line into a dict of metrics
        fields = ['ops', '1ms', '8ms', '64ms']
        for op_type in raw_lines.keys():
            metrics = dict(zip(fields, raw_lines[op_type].split(',')[1:]))

            # publish each metric
            for metric in metrics.keys():
                self.publish_gauge('latency.%s.%s' %
                                   (op_type, metric), metrics[metric])

    def collect_statistics(self, data):

        # Only gather whitelisted metrics
        gather_stats = self.config['statistics_whitelist']

        # Break data into k/v pairs
        for statline in data.split(';'):
            (stat, value) = statline.split('=')
            if stat in gather_stats:
                self.publish_gauge('statistics.%s' % stat, value)

    def collect_throughput(self, data):

        # Get individual data lines (every other output line is data)
        raw_lines = {}
        (
            raw_lines['reads'],
            raw_lines['writes_master'],
            raw_lines['proxy'],
            raw_lines['udf'],
            raw_lines['query'],
        ) = data.split(';')[1::2]

        for op_type in raw_lines.keys():
            metric = raw_lines[op_type].split(',')[1]
            self.publish_gauge('throughput.%s' % op_type, metric)

    def collect_namespace(self, namespace, data):

        # Only gather whitelisted metrics
        gather_stats = self.config['namespace_statistics_whitelist']

        # Break data into k/v pairs
        for statline in data.split(';'):
            (stat, value) = statline.split('=')
            if stat in gather_stats:
                self.publish_gauge('namespace.%s.%s' % (namespace, stat), value)

    def collect(self):

        self.log.debug('Connecting to %s:%s' %
                       (self.config['req_host'], self.config['req_port']))
        t = telnetlib.Telnet(self.config['req_host'], self.config['req_port'])

        try:

            # Only collect metrics we're asked for
            if (self.config['latency']):
                self.log.debug('Polling for latency')
                t.write('latency:\n')
                latency = t.read_until('\n', 1)
                self.collect_latency(latency)

            if (self.config['statistics']):
                self.log.debug('Polling for statistics')
                t.write('statistics\n')
                statistics = t.read_until('\n', 1)
                self.collect_statistics(statistics)

            if (self.config['throughput']):
                self.log.debug('Polling for throughput')
                t.write('throughput:\n')
                throughput = t.read_until('\n', 1)
                self.collect_throughput(throughput)

            if (self.config['namespaces']):
                self.log.debug('Polling for namespaces')
                t.write('namespaces\n')
                namespaces = t.read_until('\n', 1).strip()
                for namespace in namespaces.split(';'):

                    self.log.debug('Polling namespace: %s' % namespace)
                    # Skip namespaces not whitelisted if there is a whitelist
                    if (self.config['namespaces_whitelist'] and
                       namespace not in self.config['namespaces_whitelist']):
                        self.log.debug('Skipping non-whitelisted namespace: %s'
                                       % namespace)
                        continue

                    t.write('namespace/%s\n' % namespace)
                    namespace_data = t.read_until('\n', 1)
                    self.collect_namespace(namespace, namespace_data)

            t.close()

        except (socket.error, EOFError) as e:
            self.log.error("Unable to retrieve aerospike data: %s" % e)

        except Exception as e:
            self.log.error("Unknown failure in aerospike collection: %s" % e)
