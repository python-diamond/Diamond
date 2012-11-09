# coding=utf-8

"""
[Librato](http://librato.com) is an infrastructure software as a service company
dedicated to delivering beautiful, easy to use tools that make managing your
operations more fun and efficient.

#### Dependencies

 * SimpleJson
 * [requests](http://docs.python-requests.org/)

#### Configuration

Enable this handler

 * handers = diamond.handler.librato.LibratoHandler

 * user = LIBRATO_USERNAME
 * apikey = LIBRATO_API_KEY

"""

from Handler import Handler
import logging

try:
    import json
    json  # workaround for pyflakes issue #13
except ImportError:
    import simplejson as json

import requests
from requests.auth import HTTPBasicAuth


class LibratoHandler(Handler):

    def __init__(self, config=None):
        """
        Create a new instance of the LibratoHandler class
        """
        # Initialize Handler
        Handler.__init__(self, config)
        logging.debug("Initialized statsd handler.")
        # Initialize Options
        self.user = self.config['user']
        self.apikey = self.config['apikey']
        self.url = 'https://metrics-api.librato.com/v1/metrics'
        self.batch_size = 300
        self.batch = {
            'counters': [],
            'gauges': [],
        }

    def process(self, metric):
        """
        Process a metric by sending it to Librato
        """
        # Acquire lock
        self.lock.acquire()

        path = metric.path.replace('servers.' + metric.host + '.', '')

        data = {
            'source': metric.host,
            'name': path,
            'value': float(metric.value),
            'measure_time': metric.timestamp,
        }

        self.batch['counters'].append(data)

        if len(self.batch['counters']) >= self.batch_size:

            # Log
            self.log.debug("LibratoHandler: Sending batch size: %d",
                           self.batch_size)

            # Send json batch
            self._send()

            # Clear Batch
            self.batch = {
                'counters': [],
                'gauges': [],
            }

        # Release lock
        self.lock.release()

    def _send(self):
        """
        Send data to Librato.
        """

        self.log.debug(self.batch)

        headers = {'Content-type': 'application/json', }

        requests.post(self.url,
                      data=json.dumps(self.batch),
                      headers=headers,
                      auth=HTTPBasicAuth(self.user, self.apikey)
                      )
