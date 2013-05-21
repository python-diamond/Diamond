# coding=utf-8

"""
Send metrics to a [graphite](http://graphite.wikidot.com/) using the default
interface. Unlike GraphiteHandler, this one supports multiple graphite servers.
Specify them as a list of hosts divided by comma.
"""

from Handler import Handler
from graphite import GraphiteHandler
from copy import deepcopy


class MultiGraphiteHandler(Handler):
    """
    Implements the abstract Handler class, sending data to multiple
    graphite servers by using two instances of GraphiteHandler
    """

    def __init__(self, config=None):
        """
        Create a new instance of the MultiGraphiteHandler class
        """
        # Initialize Handler
        Handler.__init__(self, config)

        self.handlers = []

        # Initialize Options
        hosts = self.config['host']
        for host in hosts:
            config = deepcopy(self.config)
            config['host'] = host
            self.handlers.append(GraphiteHandler(config))

    def process(self, metric):
        """
        Process a metric by passing it to GraphiteHandler
        instances
        """
        for handler in self.handlers:
            handler.process(metric)

    def flush(self):
        """Flush metrics in queue"""
        for handler in self.handlers:
            handler.flush()
