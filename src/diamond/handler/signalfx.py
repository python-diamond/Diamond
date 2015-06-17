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

 * include_filters = [optional | '^.*'] A list of regex patterns.
     Only measurements whose path matches a filter will be submitted.
     Useful for limiting usage to *only* desired measurements, e.g.
       include_filters = "^diskspace\..*\.byte_avail$", "^loadavg\.01"
       include_filters = "^sockets\.",
                                     ^ note trailing comma to indicate a list
"""

from Handler import Handler
from diamond.util import get_diamond_version
import json
import logging
import time
import urllib2
import re


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
        # If a user leaves off the ending comma, cast to a array for them
        include_filters = self.config['include_filters']
        if isinstance(include_filters, basestring):
            include_filters = [include_filters]

        self.include_reg = re.compile(r'(?:%s)' % '|'.join(include_filters))

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
            'include_filters': 'Regex pattern to filter which metrics are sent',
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
            'include_filters': ['^.*'],
            })

        return config

    def process(self, metric):
        """
        Queue a metric.  Flushing queue if batch size reached
        """
        path = metric.getCollectorPath()
        path += '.'
        path += metric.getMetricPath()

        if not self.include_reg.match(path):
            # Skip metrics if not matched in include_filters
            return

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
