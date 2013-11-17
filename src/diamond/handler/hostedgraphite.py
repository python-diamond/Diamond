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
        # Initialize Handler
        Handler.__init__(self, config)

        self.key = self.config['apikey'].lower().strip()

        self.graphite = GraphiteHandler(self.config)

    def get_default_config_help(self):
        """
        Returns the help text for the configuration options for this handler
        """
        config = super(HostedGraphiteHandler, self).get_default_config_help()

        config.update({
            'apikey': 'Api key to use',
            'host': 'Hostname',
            'port': 'Port',
            'proto': 'udp or tcp',
            'timeout': '',
            'batch': 'How many to store before sending to the graphite server',
            'max_backlog_multiplier': 'how many batches to store before '
                'trimming',
            'trim_backlog_multiplier': 'Trim down how many batches',
        })

        return config

    def get_default_config(self):
        """
        Return the default config for the handler
        """
        config = super(HostedGraphiteHandler, self).get_default_config()

        config.update({
            'apikey': '',
            'host': 'carbon.hostedgraphite.com',
            'port': 2003,
            'proto': 'tcp',
            'timeout': 15,
            'batch': 1,
            'max_backlog_multiplier': 5,
            'trim_backlog_multiplier': 4,
        })

        return config

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
