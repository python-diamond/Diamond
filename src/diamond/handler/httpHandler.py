#!/usr/bin/env python
# coding=utf-8

from Handler import Handler
import urllib2


class HttpPostHandler(Handler):

# Inititalize Handler with url and batch size
    def __init__(self, config=None):
        Handler.__init__(self, config)
        self.metrics = []
        self.batch_size = int(self.config.get('batch', 100))
        self.url = self.config.get('url')

# Join batched metrics and push to url mentioned in config
    def process(self, metric):
        self.metrics.append(str(metric))
        if len(self.metrics) >= self.batch_size:
            req = urllib2.Request(self.url, "\n".join(self.metrics))
            urllib2.urlopen(req)
            self.metrics = []
