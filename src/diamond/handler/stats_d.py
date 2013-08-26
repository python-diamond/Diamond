# coding=utf-8

"""
Implements the abstract Handler class, sending data to statsd.
This is a UDP service, sending datagrams.  They may be lost.
It's OK.

#### Dependencies

 * [python-statsd](http://pypi.python.org/pypi/python-statsd/)
 * [statsd](https://github.com/etsy/statsd) v0.1.1 or newer.

#### Configuration

Enable this handler

 * handers = diamond.handler.stats_d.StatsdHandler


#### Notes

If your system has both
[python-statsd](http://pypi.python.org/pypi/python-statsd/)
and [statsd](http://pypi.python.org/pypi/statsd/) installed, you might
experience failues after python updates or pip updates that change the order of
importing. We recommend that you only have
[python-statsd](http://pypi.python.org/pypi/python-statsd/)
installed on your system if you are using this handler.

The handler file is named an odd stats_d.py because of an import issue with
having the python library called statsd and this handler's module being called
statsd, so we use an odd name for this handler. This doesn't affect the usage
of this handler.

"""

from Handler import Handler
import logging
try:
    import statsd
    statsd  # Pyflakes
except ImportError:
    pass


class StatsdHandler(Handler):

    def __init__(self, config=None):
        """
        Create a new instance of the StatsdHandler class
        """
        # Initialize Handler
        Handler.__init__(self, config)
        logging.debug("Initialized statsd handler.")
        # Initialize Options
        self.host = self.config['host']
        self.port = int(self.config['port'])
        self.batch_size = int(self.config['batch'])
        self.metrics = []
        self.old_values = {}

        # Connect
        self._connect()

    def get_default_config_help(self):
        """
        Returns the help text for the configuration options for this handler
        """
        config = super(StatsdHandler, self).get_default_config_help()

        config.update({
            'host': '',
            'port': '',
            'batch': '',
        })

        return config

    def get_default_config(self):
        """
        Return the default config for the handler
        """
        config = super(StatsdHandler, self).get_default_config()

        config.update({
            'host': '',
            'port': 1234,
            'batch': 1,
        })

        return config

    def process(self, metric):
        """
        Process a metric by sending it to statsd
        """

        self.metrics.append(metric)

        if len(self.metrics) >= self.batch_size:
            self._send()

    def _send(self):
        """
        Send data to statsd. Fire and forget.  Cross fingers and it'll arrive.
        """
        for metric in self.metrics:

            # Split the path into a prefix and a name
            # to work with the statsd module's view of the world.
            # It will get re-joined by the python-statsd module.
            (prefix, name) = metric.path.rsplit(".", 1)
            logging.debug("Sending %s %s|g", name, metric.value)

            if metric.metric_type == 'GAUGE':
                statsd.Gauge(prefix, self.connection).send(name, metric.value)
            else:
                # To send a counter, we need to just send the delta
                # but without any time delta changes
                value = metric.raw_value
                if metric.path in self.old_values:
                    value = value - self.old_values[metric.path]
                self.old_values[metric.path] = metric.raw_value
                statsd.Counter(prefix, self.connection).increment(name, value)

        self.metrics = []

    def flush(self):
        """Flush metrics in queue"""
        self._send()

    def _connect(self):
        """
        Connect to the statsd server
        """
        # Create socket
        self.connection = statsd.Connection(
            host=self.host,
            port=self.port,
            sample_rate=1.0
        )
