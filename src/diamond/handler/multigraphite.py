# coding=utf-8

"""
Send metrics to a [graphite](http://graphite.wikidot.com/) using the default
interface.

Graphite is an enterprise-scale monitoring tool that runs well on cheap
hardware. It was originally designed and written by Chris Davis at Orbitz in
2006 as side project that ultimately grew to be a foundational monitoring tool.
In 2008, Orbitz allowed Graphite to be released under the open source Apache
2.0 license. Since then Chris has continued to work on Graphite and has
deployed it at other companies including Sears, where it serves as a pillar of
the e-commerce monitoring system. Today many
[large companies](http://graphite.readthedocs.org/en/latest/who-is-using.html)
use it.

"""

from Handler import Handler
from graphite import GraphiteHandler
from copy import deepcopy


class MultiGraphiteHandler(Handler):
    """
    Implements the abstract Handler class, sending data to graphite
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
        Process a metric by sending it to graphite
        """
        for handler in self.handlers:
            handler.process(metric)

    def flush(self):
        """Flush metrics in queue"""
        for handler in self.handlers:
            handler.flush()
