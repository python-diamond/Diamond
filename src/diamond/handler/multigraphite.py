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

        # Initialize Data
        self.sockets = []

        # Initialize Options
        self.proto = self.config.get('proto', 'tcp').lower().strip()
        self.hosts = self.config['host']
        self.port = int(self.config.get('port', 2003))
        self.timeout = int(self.config.get('timeout', 15))
        self.batch_size = int(self.config.get('batch', 1))
        self.max_backlog_multiplier = int(
            self.config.get('max_backlog_multiplier', 5))
        self.trim_backlog_multiplier = int(
            self.config.get('trim_backlog_multiplier', 4))
        self.metrics = []

        # Connect
        self._connect()

    def __del__(self):
        """
        Destroy instance of the MultiGraphiteHandler class
        """
        self._close()

    def process(self, metric):
        """
        Process a metric by sending it to graphite
        """
        # Append the data to the array as a string
        self.metrics.append(str(metric))
        if len(self.metrics) >= self.batch_size:
            self._send()

    def flush(self):
        """Flush metrics in queue"""
        self._send()

    def _send_data(self, data):
        """
        Try to send all data in buffer.
        """
        for sock in self.sockets:
            if sock is None:
                # try to reconnect
                self.log.debug("MultiGraphiteHandler: Found disconnected socket. "
                               "Reconnecting.")
                self._close()
                self._connect()
            else:
                sock.sendall(data)

    def _send(self):
        """
        Send data to graphite. Data that can not be sent will be queued.
        """
        # Check to see if we have a valid socket. If not, try to connect.
        try:
            try:
                if not len(self.sockets):
                    self.log.debug("MultiGraphiteHandler: No connected sockets. "
                                   "Reconnecting.")
                    self._connect()
                if not len(self.sockets):
                    self.log.debug("MultiGraphiteHandler: Reconnect failed.")
                else:
                    # Send data to socket
                    self._send_data(''.join(self.metrics))
                    self.metrics = []
            except Exception:
                self._close()
                self.log.error("MultiGraphiteHandler: Error sending metrics.")
                raise
        finally:
            if len(self.metrics) >= (self.batch_size * self.max_backlog_multiplier):
                trim_offset = (self.batch_size
                               * self.trim_backlog_multiplier * -1)
                self.log.warn('MultiGraphiteHandler: Trimming backlog. Removing'
                              + ' oldest %d and keeping newest %d metrics',
                              len(self.metrics) - abs(trim_offset),
                              abs(trim_offset))
                self.metrics = self.metrics[trim_offset:]

    def _connect(self):
        """
        Connect to the graphite server(s)
        """
        if (self.proto == 'udp'):
            stream = socket.SOCK_DGRAM
        else:
            stream = socket.SOCK_STREAM

        for host in self.hosts:
            # Create socket
            sock = socket.socket(socket.AF_INET, stream)
            if socket is None:
                # Log Error
                self.log.error("MultiGraphiteHandler: Unable to create socket.")
                # Close Socket
                self._close()
                return
            # Set socket timeout
            sock.settimeout(self.timeout)
            # Connect to graphite server
            try:
                sock.connect((host, self.port))
                # Log
                self.log.debug("MultiGraphiteHandler: Established connection to "
                               "graphite server %s:%d.",
                               host, self.port)
            except Exception, ex:
                # Log Error
                self.log.error("MultiGraphiteHandler: Failed to connect to %s:%i. %s.",
                               host, self.port, ex)
                # Close Socket
                self._close()
                return
            self.sockets.append(sock)

    def _close(self):
        """
        Close all sockets
        """
        for socket in self.sockets:
            if socket is not None:
                socket.close()
                socket = None
