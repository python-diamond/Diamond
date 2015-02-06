# coding=utf-8

"""
Send metrics to a [graphite](http://graphite.wikidot.com/) using the high
performace pickle interface.

Graphite is an enterprise-scale monitoring tool that runs well on cheap
hardware. It was originally designed and written by Chris Davis at Orbitz in
2006 as side project that ultimately grew to be a foundational monitoring tool.
In 2008, Orbitz allowed Graphite to be released under the open source Apache
2.0 license. Since then Chris has continued to work on Graphite and has
deployed it at other companies including Sears, where it serves as a pillar of
the e-commerce monitoring system. Today many
[large companies](http://graphite.readthedocs.org/en/latest/who-is-using.html)
use it.

- enable it in `diamond.conf` :

`    handlers = diamond.handler.graphitepickle.GraphitePickleHandler
`

"""

import struct

from graphite import GraphiteHandler


class GraphitePickleHandler(GraphiteHandler):

    """
    Overrides the GraphiteHandler class
    Sending data to graphite using batched pickle format
    """

    def __init__(self, config=None):
        """
        Create a new instance of the GraphitePickleHandler
        """
        # Initialize GraphiteHandler
        GraphiteHandler.__init__(self, config)
        # Initialize Data
        # Initialize Options
        self.batch_size = int(self.config['batch'])

    def get_default_config_help(self):
        """
        Returns the help text for the configuration options for this handler
        """
        config = super(GraphitePickleHandler, self).get_default_config_help()

        config.update({
        })

        return config

    def get_default_config(self):
        """
        Return the default config for the handler
        """
        config = super(GraphitePickleHandler, self).get_default_config()

        config.update({
            'port': 2004,
        })

        return config

    def process(self, metric):
        self.metrics.append(str(metric))
        if len(self.metrics) >= self.batch_size:
            self.flush()
