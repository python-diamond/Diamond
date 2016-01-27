# coding=utf-8
"""
Diamond handler for App Enlight (https://appenlight.com/)

To work this handler need basic configuration:

[[AppenlightMetricHandler]]
apikey = PRIVATE_API_KEY
#server = http://optinal.serveraddress.com

"""

import datetime
import json
import logging
import urllib2

from collections import deque
from diamond.handler.Handler import Handler

log = logging.getLogger(__name__)


class AppenlightMetricHandler(Handler):
    def __init__(self, config=None):
        """
        New instance of MetricHandler class
        """
        Handler.__init__(self, config)
        self.apikey = self.config.get('apikey', '')
        self.server = self.config.get('server',
                                      'https://api.appenlight.com')

        self.queue_size = self.config.get('queue_size', 100)
        self.queue = deque([])

    def get_default_config_help(self):
        """
        Help text
        """
        config = super(AppenlightMetricHandler, self).get_default_config_help()

        config.update({
            'apikey': '',
            'server': 'https://api.appenlight.com',
            'queue_size': 100
        })

        return config

    def get_default_config(self):
        """
        Return default config for the handler
        """
        config = super(AppenlightMetricHandler, self).get_default_config()

        config.update({
            'apikey': '',
            'server': 'https://api.appenlight.com',
            'queue_size': 100
        })

        return config

    def process(self, metric):
        """
        Process metric
        """

        self.queue.append(metric)
        if len(self.queue) >= self.queue_size:
            self._send()

    def flush(self):
        """
        Flush metrics
        """

        self._send()

    def _send(self):
        """
        Insert the data
        """
        metrics_list = []
        while len(self.queue) > 0:
            metric = self.queue.popleft()
            namespace = '{}.{}'.format(metric.getPathPrefix(),
                                       metric.getCollectorPath())
            timestamp = datetime.datetime.utcfromtimestamp(metric.timestamp)
            metrics_list.append({
                'namespace': namespace,
                'timestamp': timestamp.strftime('%Y-%m-%dT%H:%M:%S.%f'),
                'server_name': metric.host or 'unknown',
                'tags': (('value', metric.value),
                         ('gauge', metric.metric_type),
                         ('name', metric.getMetricPath()))
            })
        if metrics_list:
            req = urllib2.Request(self.server + '/api/general_metrics',
                                  data=json.dumps(metrics_list))
            req.add_header('User-Agent', 'appenlight-diamond/0.1')
            req.add_header('Content-Type', 'application/json')
            req.add_header('X-appenlight-api-key', self.apikey.encode('utf8'))
            r = urllib2.urlopen(req, timeout=30)
