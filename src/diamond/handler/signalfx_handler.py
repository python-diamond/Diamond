# coding=utf-8

"""
Send metrics to signalfx

#### Dependencies

 * signalfx (pip install signalfx)


#### Configuration
Enable this handler

 * handlers = diamond.handler.signalfx_handler.SignalfxHandler

 * auth_token = SIGNALFX_AUTH_TOKEN

 * batch_size = [optional | 300 ] will wait for this many requests before
     posting
"""
from Handler import Handler
import collections
import logging
import time

try:
    import signalfx
except ImportError:
    raise ImportError("Failed to load signalfx module. "
                      "Install signalfx module - `pip install signalfx`")

from diamond.util import get_diamond_version


class SignalfxHandler(Handler):

    # Inititalize Handler with url and batch size
    def __init__(self, config=None):
        super(SignalfxHandler, self).__init__(config)
        self.metrics = []
        auth_token = self.config['auth_token']
        url = self.config['url']
        self.batch_size = int(self.config['batch'])
        self.batch_max_interval = float(self.config['batch_max_interval'])
        self.resetBatchTimeout()
        self.signalfx = signalfx.SignalFx(auth_token, ingest_endpoint=url,
                                          batch_size=self.batch_size,
                                          user_agents=[self.user_agent()])

    def resetBatchTimeout(self):
        self.batch_max_timestamp = time.time() + self.batch_max_interval

    def get_default_config_help(self):
        """
        Returns the help text for the configuration options for this handler
        """
        config = super(SignalfxHandler, self).get_default_config_help()

        config.update({
            'url': 'Where to send metrics',
            'batch': 'How many to store before sending',
            'auth_token': 'Org API token to use when sending metrics',
        })

        return config

    def get_default_config(self):
        """
        Return the default config for the handler
        """
        config = super(SignalfxHandler, self).get_default_config()

        config.update({
            'url': 'https://ingest.signalfx.com/',
            'batch': 300,
            # Don't wait more than 10 sec between pushes
            'batch_max_interval': 10,
            'auth_token': '',
        })

        return config

    def process(self, metric):
        """
        Queue a metric.  Flushing queue if batch size reached
        """
        self.metrics.append(metric)
        if self.should_flush():
            self._send()

    def should_flush(self):
        return len(self.metrics) >= self.batch_size or \
            time.time() >= self.batch_max_timestamp

    def into_signalfx_point(self, metric):
        """
        Convert diamond metric into something signalfx can understand
        """
        dims = {
            "collector": metric.getCollectorPath(),
            "prefix": metric.getPathPrefix(),
        }
        if metric.host is not None and metric.host != "":
            dims["host"] = metric.host

        return {
            "metric": metric.getMetricPath(),
            "value": metric.value,
            "dimensions": dims,
            # We expect ms timestamps
            "timestamp": metric.timestamp * 1000,
        }

    def flush(self):
        """Flush metrics in queue"""
        self._send()

    def user_agent(self):
        """
        HTTP user agent
        """
        return "Diamond/{}".format(get_diamond_version())

    def _send(self):
        datapoint = collections.defaultdict(list)
        for metric in self.metrics:
            datapoint[metric.metric_type.lower()].append(
                self.into_signalfx_point(metric))
        logging.debug('Body - %s', datapoint)
        self.signalfx.send(gauges=datapoint.get('gauge', {}),
                           counters=datapoint.get('counter', {}),
                           cumulative_counters=datapoint.get(
                               'cumulative_counter', {}))
        self.resetBatchTimeout()
        self.metrics = []
