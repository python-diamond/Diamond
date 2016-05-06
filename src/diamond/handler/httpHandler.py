#!/usr/bin/env python
# coding=utf-8

"""
Send metrics to a http endpoint via POST
"""

from Handler import Handler
import urllib2
import json


class HttpPostHandler(Handler):

    # Inititalize Handler with url and batch size
    def __init__(self, config=None):
        Handler.__init__(self, config)
        self.metrics = []
        self.batch_size = int(self.config['batch'])
        self.format = self.config['format']
        self.url = self.config['url']

    def get_default_config_help(self):
        """
        Returns the help text for the configuration options for this handler
        """
        config = super(HttpPostHandler, self).get_default_config_help()

        config.update({
            'url': 'Fully qualified url to send metrics to',
            'format': 'Format to send metrics (PLAIN or JSON)',
            'batch': 'How many to store before sending to the graphite server',
        })

        return config

    def get_default_config(self):
        """
        Return the default config for the handler
        """
        config = super(HttpPostHandler, self).get_default_config()

        config.update({
            'url': 'http://localhost/blah/blah/blah',
            'format': 'PLAIN',
            'batch': 100,
        })

        return config

    # Join batched metrics and push to url mentioned in config
    def process(self, metric):
        self.metrics.append(metric)
        if len(self.metrics) >= self.batch_size:
            self.post()

    # Overriding flush to post metrics for every collector.
    def flush(self):
        """Flush metrics in queue"""
        self.post()

    def post(self):
        if self.format == 'JSON':
            header = {
                'Content-type': 'application/json',
                'Accept': 'application/json'
            }
            json_fmt = dict(metric=[])
            for metric in self.metrics:
                json_fmt['metric'].append(dict(
                    path=metric.path,
                    value=metric.value,
                    timestamp=metric.timestamp,
                    precision=metric.precision,
                    host=metric.host,
                    ttl=metric.ttl
                ))
            req = urllib2.Request(self.url,
                                  json.dumps(json_fmt),
                                  headers=header)
        else:
            # Default to PLAIN if nor JSON
            req = urllib2.Request(self.url,
                                  "\n".join([str(m) for m in self.metrics]))

        urllib2.urlopen(req)
        self.metrics = []
