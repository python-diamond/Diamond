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
from distutils.version import LooseVersion


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
            # 2.7 Stats
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
            # 3.9 Stats
            'objects',
            'cluster_size',
            'system_free_mem_pct',
            'client_connections',
            'scans_active',
        ]
        default_config['namespace_statistics_whitelist'] = [
            # 2.7 Stats
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
            # 3.9 Stats
            "client_delete_error",
            "client_delete_success",
            "client_read_error",
            "client_read_success",
            "client_write_error",
            "client_write_success",
            "device_available_pct",
            "device_free_pct",
            "device_total_bytes",
            "device_used_bytes",
            "expired_objects",
            "evicted_objects",
            "memory-size",
            "memory_free_pct",
            "memory_used_bytes",
            "memory_used_data_bytes",
            "memory_used_index_bytes",
            "memory_used_sindex_bytes",
            "migrate_rx_partitions_active",
            "migrate_rx_partitions_initial",
            "migrate_rx_partitions_remaining",
            "migrate_tx_partitions_active",
            "migrate_tx_partitions_initial",
            "migrate_tx_partitions_remaining",
            "objects",
        ]
        default_config['path'] = 'aerospike'

        return default_config

    def collect_latency(self, data):

        fields = ['ops', '1ms', '8ms', '64ms']

        if self.config['dialect'] >= 39:
            # Get "header" section of each histogram
            labels = data.split(';')[::2]
            # Get contents of histogram
            datasets = data.split(';')[1::2]
            for i, label in enumerate(labels):
                # Extract namespace and histogram type from header label
                match = re.match('\{(\w+)\}-(\w+)', label)
                if match:
                    namespace = match.group(1)
                    histogram = match.group(2)

                    # Create metrics dict for the namespace/histogram pair
                    dataset = datasets[i].split(',')[1:]
                    metrics = dict(zip(fields, dataset))

                    # Publish a metric for each field in the histogram
                    for field in fields:
                        self.publish_gauge('latency.%s.%s.%s' %
                                           (namespace, histogram, field),
                                           metrics[field])

        elif self.config['dialect'] < 39:
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

        if self.config['dialect'] >= 39:
            # Get "header" section of each histogram
            labels = data.split(';')[::2]
            # Get contents of histogram
            datasets = data.split(';')[1::2]
            for i, label in enumerate(labels):
                # Extract namespace and histogram type from header label
                match = re.match('\{(\w+)\}-(\w+)', label)
                if match:
                    namespace = match.group(1)
                    histogram = match.group(2)

                    # Exctract metric from dataset
                    metric = datasets[i].split(',')[1]

                    self.publish_gauge('throughput.%s.%s' %
                                       (namespace, histogram), metric)

        elif self.config['dialect'] < 39:
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

            # Detect the version of aerospike for later
            self.log.debug('Checking aerospike version')
            t.write('version\n')
            version = t.read_until('\n', 1)
            if LooseVersion(version) >= LooseVersion("3.9"):
                self.config['dialect'] = 39
            else:
                self.config['dialect'] = 27

            self.log.debug('Got version %s and selecting dialect %s' %
                           (version, self.config['dialect']))

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
