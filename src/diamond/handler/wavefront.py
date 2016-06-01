# coding=utf-8

"""
A handler to send metrics to a Wavefront proxy. Derived from the
OpenTSDB handler, as the two protocols are very similar. Tested with the
Wavefront Test Proxy.

Wavefront has the concept of "point tags": these are key=value pairs
which apply to individual points. You can add point tags in the Handler
configuration stanza:

    [[WavefrontHandler]]
    port = 2878
    tags = mytag1=myval1,mytag2=myval2

in which case they will be applied to all points the handler sends.

You can also set point tags through the publish() method in your
collector, using the `point_tags` parameter, with a dict as the
argument.

    self.publish('metric', value, point_tags={'mytag1': 'myval1',
                                              'mytag2': 'myval2',})

Both the key and value will automatically be wrapped in soft quotes.

This handler will *not* speak directly to the Wavefront API: that is a
different problem.
"""

from Handler import Handler
import socket
import re


class WavefrontHandler(Handler):
    RETRY = 3

    def __init__(self, config=None):
        """
        Create a new instance of the WavefrontHandler class
        """
        # Initialize Handler
        Handler.__init__(self, config)

        # Initialize Data
        self.socket = None

        # Initialize Options
        self.host = self.config['host']
        self.port = int(self.config['port'])
        self.timeout = int(self.config['timeout'])
        self.metric_format = str(self.config['format'])
        self.tags = self.process_handler_tags(self.config['tags'])

        # Connect
        self._connect()

    def process_handler_tags(self, tags):
        """
        These tags come to us via the handler config. Might be a string,
        might be a list
        :returns: a list of key=value pairs
        """

        if isinstance(tags, list):
            ret = tags
        elif (isinstance(tags, basestring) and tags != ''):
            ret = [tags]
        else:
            ret = []

        return self.quote_point_tags(ret)

    def process_point_tags(self, tags):
        """
        These tags come to us as part of a Metric object. They are a
        dict.

        :returns: a list of key=value pairs
        """
        if not isinstance(tags, dict):
            return []

        return self.quote_point_tags(['%s="%s"' % (k, v) for k, v in
                                     tags.items()])

    def quote_point_tags(self, tags):
        """
        Wavefront allows any characters in point tags, but they need to
        be quoted. We'll be kind and quote them for the user, and also
        throw away tags which aren't a k=v pair.
        """
        ret = []

        for t in tags:
            try:
                k, v = t.split('=', 1)
                if not re.match('^".*"$', k):
                    k = '"%s"' % k

                if not re.match('^".*"$', v):
                    v = '"%s"' % v
            except:
                continue

            ret.append('%s=%s' % (k, v))

        return ret

    def get_default_config_help(self):
        """
        Returns the help text for the configuration options for this handler
        """
        config = super(WavefrontHandler, self).get_default_config_help()

        config.update({
            'host': '',
            'port': '',
            'timeout': '',
            'format': '',
            'tags': '',
        })

        return config

    def get_default_config(self):
        """
        Return the default config for the handler
        """
        config = super(WavefrontHandler, self).get_default_config()

        config.update({
            'host': '',
            'port': 2878,
            'timeout': 5,
            'format': '{Collector}.{Metric} {value} {timestamp} source={host}'
                      ' {tags}',
            'tags': '',
        })

        return config

    def __del__(self):
        """
        Destroy instance of the WavefrontHandler class
        """
        self._close()

    def process(self, metric):
        """
        Send a metric to the Wavefront proxy. Currently the Test Proxy
        has issues with exponential notation, but the real proxies
        appear not to.
        """

        metric_str = self.metric_format.format(
            Collector=metric.getCollectorPath(),
            Path=metric.path,
            Metric=metric.getMetricPath(),
            host=metric.host,
            timestamp=metric.timestamp,
            value=metric.value,
            tags=' '.join(self.tags +
                          self.process_point_tags(metric.point_tags))
        )
        # Just send the data as a string

        self._send(str(metric_str) + "\n")

    def _send(self, data):
        """
        Send data to Wavefront. Data that can not be sent will be queued.
        """
        retry = self.RETRY
        # Attempt to send any data in the queue
        while retry > 0:
            # Check socket
            if not self.socket:
                # Log Error
                self.log.error("WavefrontHandler: Socket unavailable.")
                # Attempt to restablish connection
                self._connect()
                # Decrement retry
                retry -= 1
                # Try again
                continue
            try:
                # Send data to socket
                self.socket.sendall(data)
                # Done
                break
            except socket.error, e:
                # Log Error
                self.log.error("WavefrontHandler: Failed sending data. %s.", e)
                # Attempt to restablish connection
                self._close()
                # Decrement retry
                retry -= 1
                # try again
                continue

    def _connect(self):
        """
        Connect to a Wavefront proxy
        """
        # Create socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if socket is None:
            # Log Error
            self.log.error("WavefrontHandler: Unable to create socket.")
            # Close Socket
            self._close()
            return
        # Set socket timeout
        self.socket.settimeout(self.timeout)
        # Connect to graphite server
        try:
            self.socket.connect((self.host, self.port))
            # Log
            self.log.debug("Established connection to Wavefront proxy %s:%d",
                           self.host, self.port)
        except Exception, ex:
            # Log Error
            self.log.error("WavefrontHandler: Failed to connect to %s:%i. %s",
                           self.host, self.port, ex)
            # Close Socket
            self._close()
            return

    def _close(self):
        """
        Close the socket
        """
        if self.socket is not None:
            self.socket.close()
        self.socket = None
