# coding=utf-8

"""
[Hosted Graphite](https://www.hostedgraphite.com/) is the powerful open-source
application metrics system used by hundreds of companies. We take away the
headaches of scaling, maintenance, and upgrades and let you do what you do
best - write great software.

#### Configuration

Enable this handler

 * handlers = diamond.handler.hostedgraphite.HostedGraphiteHandler,

 * apikey = API_KEY

"""

from Handler import Handler
from graphite import GraphiteHandler


class HostedGraphiteHandler(Handler):

    def __init__(self, config=None):
        """
        Create a new instance of the HostedGraphiteHandler class
        """
        self.key = config['apikey'].lower().strip()

        config['host'] = 'carbon.hostedgraphite.com'
        config['port'] = '2003'

        self.graphite = GraphiteHandler(config)

    def process(self, metric):
        """
        Process a metric by sending it to graphite
        """
        metric = self.key + '.' + str(metric)
        self.graphite.process(metric)

    def _process(self, metric):
        """
        Process a metric by sending it to graphite
        """
        metric = self.key + '.' + str(metric)
        self.graphite._process(metric)

    def _flush(self):
        self.graphite._flush()

    def flush(self):
        self.graphite.flush()
