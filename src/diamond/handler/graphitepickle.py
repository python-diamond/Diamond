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

try:
    import cPickle as pickle
    pickle  # workaround for pyflakes issue #13
except ImportError:
    import pickle as pickle


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
        self.batch = []
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
        })

        return config

    def process(self, metric):
        # Convert metric to pickle format
        m = (metric.path, (metric.timestamp, metric.value))
        # Add the metric to the match
        self.batch.append(m)
        # If there are sufficient metrics, then pickle and send
        if len(self.batch) >= self.batch_size:
            # Log
            self.log.debug("GraphitePickleHandler: Sending batch size: %d",
                           self.batch_size)
            # Pickle the batch of metrics
            self.metrics = [self._pickle_batch()]
            # Send pickled batch
            self._send()
            # Flush the metric pack down the wire
            self.flush()
            # Clear Batch
            self.batch = []

    def _pickle_batch(self):
        """
        Pickle the metrics into a form that can be understood
        by the graphite pickle connector.
        """
        # Pickle
        payload = pickle.dumps(self.batch)

        # Pack Message
        header = struct.pack("!L", len(payload))
        message = header + payload

        # Return Message
        return message
