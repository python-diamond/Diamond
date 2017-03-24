# coding=utf-8

"""
Send metrics to [Riemann](http://aphyr.github.com/riemann/).

#### Dependencies

 * [riemann-client](https://github.com/borntyping/python-riemann-client).

#### Configuration

Add `diamond.handler.riemann.RiemannHandler` to your handlers.
It has these options:

 * `host` - The Riemann host to connect to.
 * `port` - The port it's on.
 * `transport` - Either `tcp` or `udp`. (default: `tcp`)

"""

from . Handler import Handler
import logging

try:
    from riemann_client.transport import TCPTransport, UDPTransport
    from riemann_client.client import Client
    riemann_client = True
except ImportError:
    riemann_client = None


class RiemannHandler(Handler):

    def __init__(self, config=None):
        # Initialize Handler
        Handler.__init__(self, config)

        if riemann_client is None:
            logging.error("Failed to load riemann_client module")
            return

        # Initialize options
        self.host = self.config['host']
        self.port = int(self.config['port'])
        self.transport = self.config['transport']

        # Initialize client
        if self.transport == 'tcp':
            self.transport = TCPTransport(self.host, self.port)
        else:
            self.transport = UDPTransport(self.host, self.port)
        self.client = Client(self.transport)
        self._connect()

    def get_default_config_help(self):
        """
        Returns the help text for the configuration options for this handler
        """
        config = super(RiemannHandler, self).get_default_config_help()

        config.update({
            'host': '',
            'port': '',
            'transport': 'tcp or udp',
        })

        return config

    def get_default_config(self):
        """
        Return the default config for the handler
        """
        config = super(RiemannHandler, self).get_default_config()

        config.update({
            'host': '',
            'port': 123,
            'transport': 'tcp',
        })

        return config

    def process(self, metric):
        """
        Send a metric to Riemann.
        """
        event = self._metric_to_riemann_event(metric)
        try:
            self.client.send_event(event)
        except Exception as e:
            self.log.error(
                "RiemannHandler: Error sending event to Riemann: %s", e)

    def _metric_to_riemann_event(self, metric):
        """
        Convert a metric to a dictionary representing a Riemann event.
        """
        # Riemann has a separate "host" field, so remove from the path.
        path = '%s.%s.%s' % (
            metric.getPathPrefix(),
            metric.getCollectorPath(),
            metric.getMetricPath()
        )

        return self.client.create_event({
            'host': metric.host,
            'service': path,
            'time': metric.timestamp,
            'metric_f': float(metric.value),
            'ttl': metric.ttl,
        })

    def _connect(self):
        self.transport.connect()

    def _close(self):
        """
        Disconnect from Riemann.
        """
        if hasattr(self, 'transport'):
            self.transport.disconnect()

    def __del__(self):
        self._close()
