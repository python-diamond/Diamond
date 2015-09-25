# coding=utf-8

"""
Send metrics to signalfx

#### Dependencies

 * urllib2


#### Configuration
Enable this handler

 * handers = diamond.handler.httpHandler.SignalfxHandler

 * auth_token = SIGNALFX_AUTH_TOKEN
 * batch_size = [optional | 300 ] will wait for this many requests before
     posting
"""

from Handler import Handler
from diamond.util import get_diamond_version
import json
import logging
import time
import urllib2


class SignalfxHandler(Handler):

    # Inititalize Handler with url and batch size
    def __init__(self, config=None):
        Handler.__init__(self, config)
        self.metrics = []
        self.batch_size = int(self.config['batch'])
        self.url = self.config['url']
        self.auth_token = self.config['auth_token']
        self.batch_max_interval = self.config['batch_max_interval']
        self.resetBatchTimeout()
        if self.auth_token == "":
            logging.error("Failed to load Signalfx module")
            return

    def resetBatchTimeout(self):
        self.batch_max_timestamp = int(time.time() + self.batch_max_interval)

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
            'url': 'https://ingest.signalfx.com/v2/datapoint',
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
        return "Diamond: %s" % get_diamond_version()

    def _send(self):
        # Potentially use protobufs in the future
        postDictionary = {}
        for metric in self.metrics:
            t = metric.metric_type.lower()
            if t not in postDictionary:
                postDictionary[t] = []
            postDictionary[t].append(self.into_signalfx_point(metric))

        self.metrics = []
        postBody = json.dumps(postDictionary)
        logging.debug("Body is %s", postBody)
        req = urllib2.Request(self.url, postBody,
                              {"Content-type": "application/json",
                               "X-SF-TOKEN": self.auth_token,
                               "User-Agent": self.user_agent()})
        self.resetBatchTimeout()
        try:
            urllib2.urlopen(req)
        except urllib2.URLError:
            logging.exception("Unable to post signalfx metrics")
            return
