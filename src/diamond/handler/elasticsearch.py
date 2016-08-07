# coding=utf-8

"""
Send metric to [Elasticsearch] cluster
(https://www.elastic.co/products/elasticsearch) using bulk API.

Require python Elastic client
"""

from diamond.handler.Handler import Handler
from elasticsearch.client import Elasticsearch

from datetime import datetime
try:
    import json
except ImportError:
    import simplejson as json


class ElasticsearchHandler(Handler):
    """
    Implements the abstract Handler class, sending data to "whatever"
    """

    def __init__(self, config=None):
        """
        Create a new instance of the ElasticsearchHandler class
        """
        # Initialize Handler
        Handler.__init__(self, config)

        # Initialize Data
        self.elasticclient = None

        # Initialize Elasticsearch client Options
        self.hosts = self.config['hosts']

        self.use_ssl = bool(self.config['use_ssl'])
        self.verify_certs = bool(self.config['verify_certs'])
        self.ca_certs = self.config['ca_certs']

        self.sniffer_timeout = int(self.config['sniffer_timeout'])
        self.sniff_on_start = bool(self.config['sniff_on_start'])
        self.sniff_on_connection_fail = bool(
            self.config['sniff_on_connection_fail'])

        self.metric_index = self.config['metric_index']
        self.index_rotation = self.config['index_rotation']
        self.request_timeout = int(self.config['request_timeout'])

        # Initialize collector options
        self.batch_size = int(self.config['batch'])
        self.max_backlog_multiplier = int(
            self.config['max_backlog_multiplier'])
        self.trim_backlog_multiplier = int(
            self.config['trim_backlog_multiplier'])

        self.metrics = []

        # Connect
        self._connect()

    def get_default_config_help(self):
        """
        Returns the help text for the configuration options for this handler
        """
        config = super(ElasticsearchHandler, self).get_default_config_help()

        config.update({
            'hosts': "Elasticsearch cluster front HTTP URL's",
            'use_ssl': 'Elasticsearch client option :'
                ' use SSL on HTTP connections',
            'verify_certs': 'Elasticsearch client option :'
                ' verify certificates.',
            'ca_certs': 'Elasticsearch client option :'
                ' path to ca_certs on disk',
            'sniffer_timeout': 'Elasticsearch client option',
            'sniff_on_start': 'Elasticsearch client option',
            'sniff_on_connection_fail': 'Elasticsearch client option',
            'metric_index': 'Elasticsearch index to store metrics',
            'index_rotation': 'Determine index name time suffix'
                ' (None|"daily"|"hourly")',
            'request_timeout': 'Elasticsearch client option',
            'batch': 'How many metrics to store before sending',
            'max_backlog_multiplier': 'how many batches to store before trimming',  # NOQA
            'trim_backlog_multiplier': 'Trim down how many batches',
        })

        return config

    def get_default_config(self):
        """
        Return the default config for the handler
        """
        config = super(ElasticsearchHandler, self).get_default_config()

        config.update({
            'hosts': ["http://127.0.0.1:9200"],
            'use_ssl': False,
            'verify_certs': False,
            'ca_certs': '',
            'sniffer_timeout': 30,
            'sniff_on_start': True,
            'sniff_on_connection_fail': True,
            'metric_index': 'metrics',
            'index_rotation': 'daily',
            'request_timeout': 30,
            'batch': 1,
            'max_backlog_multiplier': 5,
            'trim_backlog_multiplier': 4,
        })

        return config

    def __del__(self):
        """
        Destroy instance of the ElasticsearchHandler class
        """
        self._close()

    def process(self, metric):
        """
        Process a metric by storing it
        Trigger sending is batch size reached
        """
        # Append the data to the array as a string
        self.metrics.append(metric)
        if len(self.metrics) >= self.batch_size:
            self._send()

    def flush(self):
        """Flush metrics in queue"""
        self._send()

    def _send_data(self):
        """
        Try to send all data in buffer.
        """
        requests = []
        for metric in self.metrics:
            if self.index_rotation == 'daily':
                index = "%s-%s" % (
                    self.metric_index,
                    datetime.fromtimestamp(
                        metric.timestamp).strftime('%Y.%m.%d')
                )
            elif self.index_rotation == 'hourly':
                index = "%s-%s" % (
                    self.metric_index,
                    datetime.fromtimestamp(
                        metric.timestamp).strftime('%Y.%m.%d.%H')
                )
            else:
                index = self.metric_index

            requests.append(
                '{"index": {"_index": "%s", "_type": "metric", "_id": "%s_%s"}}'
                % (index, str(metric.timestamp), metric.path)
            )
            requests.append(
                '{' +
                '"timestamp": %i000, ' % metric.timestamp +
                '"path": "%s", ' % metric.path +
                '"value": %s, ' % metric.get_formatted_value() +
                '"host": "%s", ' % metric.host +
                '"metric_type": "%s", ' % metric.metric_type +
                '"raw_value": "%s", ' % str(metric.raw_value) +
                '"ttl": %s' % metric.ttl +
                '}'
            )

        if len(requests) > 0:
            res = self.elasticclient.bulk(
                "\n".join(requests),
            )

            if res['errors']:
                self.log.debug("ElasticsearchHandler: Bulk request failed"
                               " with %s" % json.dumps(res))
                self.log.error("ElasticsearchHandler: send data failed")
                raise Exception("Elasticsearch Cluster returned problem")

    def _send(self):
        """
        Send data. Data that can not be sent will be queued.
        """
        # Check to see if we have a valid connection. If not, try to connect.
        try:
            try:
                if self.elasticclient is None:
                    self.log.debug("ElasticsearchHandler: not connected. "
                                   "Reconnecting.")
                    self._connect()

                if self.elasticclient is None:
                    self.log.debug("ElasticsearchHandler: Reconnect failed.")
                else:
                    # Send data
                    self._send_data()
                    self.metrics = []
            except Exception:
                self._throttle_error("ElasticsearchHandler: "
                                     "Error sending metrics.")
        finally:
            if len(self.metrics) >= (
                    self.batch_size * self.max_backlog_multiplier):
                trim_offset = (self.batch_size *
                               self.trim_backlog_multiplier * -1)
                self.log.warn('ElasticsearchHandler: Trimming backlog. '
                              'Removing oldest %d and '
                              'keeping newest %d metrics',
                              len(self.metrics) - abs(trim_offset),
                              abs(trim_offset))
                self.metrics = self.metrics[trim_offset:]

    def _connect(self):
        """
        Connect to the server
        """
        # Connect to server
        try:
            self.elasticclient = Elasticsearch(
                self.hosts,
                use_ssl=self.use_ssl,
                verify_certs=self.verify_certs,
                ca_certs=self.ca_certs,
                sniffer_timeout=self.sniffer_timeout,
                sniff_on_start=self.sniff_on_start,
                sniff_on_connection_fail=self.sniff_on_connection_fail,
            )
            # Log
            self.log.debug("ElasticsearchHandler: Established connection to "
                           "Elasticsearch cluster %s",
                           repr(self.hosts))
        except Exception, ex:
            # Log Error
            self._throttle_error("ElasticsearchHandler: Failed to connect to "
                                 "%s.", ex)
            # Close Socket
            self._close()
            return

    def _close(self):
        """
        Close / Free
        """
        self.elasticclient = None
