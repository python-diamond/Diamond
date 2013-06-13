# coding=utf-8

"""
Send metrics to a [graphite](http://graphite.wikidot.com/) using the pickle
interface. Unlike GraphitePickleHandler, this one supports multiple graphite
servers. Specify them as a list of hosts divided by comma.
"""

from Handler import Handler
from graphitepickle import GraphitePickleHandler
from copy import deepcopy


class MultiGraphitePickleHandler(Handler):
    """
    Implements the abstract Handler class, sending data to multiple
    graphite servers by using two instances of GraphitePickleHandler
    """

    def __init__(self, config=None):
        """
        Create a new instance of the MultiGraphitePickleHandler class
        """
        # Initialize Handler
        Handler.__init__(self, config)

        self.handlers = []

        # Initialize Options
        hosts = self.config['host']
        for host in hosts:
            config = deepcopy(self.config)
            config['host'] = host
            self.handlers.append(GraphitePickleHandler(config))

    def process(self, metric):
        """
        Process a metric by passing it to GraphitePickleHandler
        instances
        """
        for handler in self.handlers:
            handler.process(metric)

    def flush(self):
        """Flush metrics in queue"""
        for handler in self.handlers:
            handler.flush()
