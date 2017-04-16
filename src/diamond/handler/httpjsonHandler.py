#!/usr/bin/env python
# coding=utf-8

"""
Send metrics in JSON to a http endpoint via POST

# Dependencies

 * urllib2


# Configuration
Enable this handler

 * handers = diamond.handler.httpjsonHandler.HttpJSONPostHandler

 * url = http://www.example.com/endpoint

"""

from Handler import Handler
import logging
import urllib2
import json


class HttpJSONPostHandler(Handler):

    # Inititalize Handler with url and batch size
    def __init__(self, config=None):
        Handler.__init__(self, config)
        self.metrics = []
        self.batch_size = int(self.config['batch'])
        self.url = self.config.get('url')

    def get_default_config_help(self):
        """
        Returns the help text for the configuration options for this handler
        """
        config = super(HttpJSONPostHandler, self).get_default_config_help()

        config.update({
            'url': 'Fully qualified url to send metrics to',
            'batch':
            'How many to store before sending to the graphite server',
            'headers':
            'Header variable if needed. Will be added to every request',
            'max_backlog_multiplier': 'how many batches to store before trimming',  # NOQA
            'trim_backlog_multiplier': 'Trim down how many batches',
        })

        return config

    def get_default_config(self):
        """
        Return the default config for the handler
        """
        config = super(HttpJSONPostHandler, self).get_default_config()

        config.update({
            'url': 'http://httpbin.org/post',
            'batch': 100,
            'headers': {'User-Agent': 'Diamond HTTP JSON Handler'},
            'max_backlog_multiplier': 5,
            'trim_backlog_multiplier': 4,
        })

        return config

    # Join batched metrics and push to url mentioned in config
    def process(self, metric):

        self.metrics.append({
            'name': metric.path,
            'value': metric.value,
            'raw_value': metric.raw_value,
            'timestamp': metric.timestamp,
            'metric_type': metric.metric_type,
            'precision': metric.precision,
            'host': metric.host,
            'ttl': metric.ttl,
            'path_prefix': metric.getPathPrefix(),
            'collector_path': metric.getCollectorPath(),
            'metric_path': metric.getMetricPath(),
        })

        if len(self.metrics) >= self.batch_size:
            self.post()

    # Overriding flush to post metrics for every collector.
    def flush(self):
        """Flush metrics in queue"""
        self.post()

    def post(self):
        # Don't let too many metrics back up
        if len(self.metrics) >= (
                self.batch_size * self.max_backlog_multiplier):
            trim_offset = (self.batch_size
                           * self.trim_backlog_multiplier * -1)
            self.log.warn('HttpPostHandler: Trimming backlog. Removing'
                          + ' oldest %d and keeping newest %d metrics',
                          len(self.metrics) - abs(trim_offset),
                          abs(trim_offset))
            self.metrics = self.metrics[trim_offset:]
        req = urllib2.Request(self.url,
                              json.dumps((self.metrics)),
                              headers=self.config['headers'])

        if 'Content-type' not in self.config['headers']:
            req.add_header('Content-type', 'application/json')

        resp = urllib2.urlopen(req)
        self.metrics = []
