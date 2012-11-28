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
import socket


class GraphiteHandler(Handler):
    """
    Implements the abstract Handler class, sending data to graphite
    """


    def __init__(self, config=None):
        """
        Create a new instance of the GraphiteHandler class
        """
        # Initialize Handler
        Handler.__init__(self, config)

        # Initialize Data
        self.socket = None

        # Initialize Options
        self.host = self.config['host']
        self.port = int(self.config['port'])
        self.timeout = int(self.config['timeout'])
        self.batch = int(self.config['batch'])
        self.metrics = []

        # Connect
        self._connect()


    def __del__(self):
        """
        Destroy instance of the GraphiteHandler class
        """
        self._close()


    def process(self, metric):
        """
        Process a metric by sending it to graphite
        """
        # Append the data to the array as a string
        self.metrics.append(str(metric))
        if len(self.metrics) >= self.batch:
            self.log.info("GraphiteHandler: Sending metrics. Graphite batch size is %s." % (len(self.metrics)))
            self._send()


    def flush(self):
        """Flush metrics in queue"""
        self.log.info("GraphiteHandler: Flush invoked. Batch size is %s." % (len(self.metrics)))
        self._send()


    def _send(self):
        """
        Send data to graphite. Data that can not be sent will be queued.
        """
        # Check to see if we have a valid socket. If not, try to connect.
        try:
            if self.socket is None:
                self.log.debug("GraphiteHandler: Socket is not connected. Reconnecting.")
                self._connect()
            # Send data to socket
            self.socket.sendall("\n".join(self.metrics))
            self.log.info("GraphiteHandler: Metrics sent.")
        except Exception:
            self._close()
            self.log.error("GraphiteHandler: Error sending metrics.")
            raise
        finally:
            # Clear metrics no matter what the result
            self.metrics = []


    def _connect(self):
        """
        Connect to the graphite server
        """
        # Create socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if socket is None:
            # Log Error
            self.log.error("GraphiteHandler: Unable to create socket.")
            # Close Socket
            self._close()
            return
        # Set socket timeout
        self.socket.settimeout(self.timeout)
        # Connect to graphite server
        try:
            self.socket.connect((self.host, self.port))
            # Log
            self.log.debug("GraphiteHandler: Established connection to graphite server %s:%d.",
                           self.host, self.port)
        except Exception, ex:
            # Log Error
            self.log.error("GraphiteHandler: Failed to connect to %s:%i. %s.",
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
