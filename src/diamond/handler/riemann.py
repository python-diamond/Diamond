# coding=utf-8

"""
Send metrics to [Riemann](http://aphyr.github.com/riemann/).

#### Dependencies

 * [Bernhard](https://github.com/banjiewen/bernhard).

#### Configuration

Add `diamond.handler.riemann.RiemannHandler` to your handlers.
It has these options:

 * `host` - The Riemann host to connect to.
 * `port` - The port it's on.
 * `transport` - Either `tcp` or `udp`. (default: `tcp`)

"""

from Handler import Handler
import logging
try:
    import bernhard
except ImportError:
    bernhard = None


class RiemannHandler(Handler):
    def __init__(self, config=None):
        # Initialize Handler
        Handler.__init__(self, config)

        if bernhard is None:
            logging.error("Failed to load bernhard module")
            return

        # Initialize options
        self.host = self.config['host']
        self.port = int(self.config['port'])
        self.transport = self.config['transport']

        # Initialize client
        if self.transport == 'tcp':
            transportCls = bernhard.TCPTransport
        else:
            transportCls = bernhard.UDPTransport
        self.client = bernhard.Client(self.host, self.port, transportCls)

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
            self.client.send(event)
        except Exception, e:
            self.log.error("RiemannHandler: Error sending event to Riemann: %s",
                           e)

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

        return {
            'host': metric.host,
            'service': path,
            'time': metric.timestamp,
            'metric': float(metric.value),
            'ttl': metric.ttl,
        }

    def _close(self):
        """
        Disconnect from Riemann.
        """
        try:
            self.client.disconnect()
        except AttributeError:
            pass

    def __del__(self):
        self._close()
