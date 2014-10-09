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
        self.proto = self.config['proto'].lower().strip()
        self.host = self.config['host']
        self.port = int(self.config['port'])
        self.timeout = int(self.config['timeout'])
        self.keepalive = bool(self.config['keepalive'])
        self.keepaliveinterval = int(self.config['keepaliveinterval'])
        self.batch_size = int(self.config['batch'])
        self.max_backlog_multiplier = int(
            self.config['max_backlog_multiplier'])
        self.trim_backlog_multiplier = int(
            self.config['trim_backlog_multiplier'])
        self.flow_info = self.config['flow_info']
        self.scope_id = self.config['scope_id']
        self.metrics = []

        # Connect
        self._connect()

    def get_default_config_help(self):
        """
        Returns the help text for the configuration options for this handler
        """
        config = super(GraphiteHandler, self).get_default_config_help()

        config.update({
            'host': 'Hostname',
            'port': 'Port',
            'proto': 'udp, udp4, udp6, tcp, tcp4, or tcp6',
            'timeout': '',
            'batch': 'How many to store before sending to the graphite server',
            'max_backlog_multiplier': 'how many batches to store before trimming',  # NOQA
            'trim_backlog_multiplier': 'Trim down how many batches',
            'keepalive': 'Enable keepalives for tcp streams',
            'keepaliveinterval': 'How frequently to send keepalives',
            'flow_info': 'IPv6 Flow Info',
            'scope_id': 'IPv6 Scope ID',
        })

        return config

    def get_default_config(self):
        """
        Return the default config for the handler
        """
        config = super(GraphiteHandler, self).get_default_config()

        config.update({
            'host': 'localhost',
            'port': 2003,
            'proto': 'tcp',
            'timeout': 15,
            'batch': 1,
            'max_backlog_multiplier': 5,
            'trim_backlog_multiplier': 4,
            'keepalive': 0,
            'keepaliveinterval': 10,
            'flow_info': 0,
            'scope_id': 0,
        })

        return config

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
        if len(self.metrics) >= self.batch_size:
            self._send()

    def flush(self):
        """Flush metrics in queue"""
        self._send()

    def _send_data(self, data):
        """
        Try to send all data in buffer.
        """
        try:
            self.socket.sendall(data)
            self._reset_errors()
        except:
            self._close()
            self._throttle_error("GraphiteHandler: Socket error, "
                                 "trying reconnect.")
            self._connect()
            try:
                self.socket.sendall(data)
            except:
                return
            self._reset_errors()

    def _send(self):
        """
        Send data to graphite. Data that can not be sent will be queued.
        """
        # Check to see if we have a valid socket. If not, try to connect.
        try:
            try:
                if self.socket is None:
                    self.log.debug("GraphiteHandler: Socket is not connected. "
                                   "Reconnecting.")
                    self._connect()
                if self.socket is None:
                    self.log.debug("GraphiteHandler: Reconnect failed.")
                else:
                    # Send data to socket
                    self._send_data(''.join(self.metrics))
                    self.metrics = []
            except Exception:
                self._close()
                self._throttle_error("GraphiteHandler: Error sending metrics.")
                raise
        finally:
            if len(self.metrics) >= (
                    self.batch_size * self.max_backlog_multiplier):
                trim_offset = (self.batch_size
                               * self.trim_backlog_multiplier * -1)
                self.log.warn('GraphiteHandler: Trimming backlog. Removing'
                              + ' oldest %d and keeping newest %d metrics',
                              len(self.metrics) - abs(trim_offset),
                              abs(trim_offset))
                self.metrics = self.metrics[trim_offset:]

    def _connect(self):
        """
        Connect to the graphite server
        """
        if (self.proto == 'udp'):
            stream = socket.SOCK_DGRAM
        else:
            stream = socket.SOCK_STREAM

        if (self.proto[-1] == '4'):
            family = socket.AF_INET
            connection_struct = (self.host, self.port)
        elif (self.proto[-1] == '6'):
            family = socket.AF_INET6
            connection_struct = (self.host, self.port,
                                 self.flow_info, self.scope_id)
        else:
            connection_struct = (self.host, self.port)
            try:
                addrinfo = socket.getaddrinfo(self.host, self.port, 0, stream)
            except socket.gaierror, ex:
                self.log.error("GraphiteHandler: Error looking up graphite host"
                               " '%s' - %s",
                               self.host, ex)
                return
            if (len(addrinfo) > 0):
                family = addrinfo[0][0]
                if (family == socket.AF_INET6):
                    connection_struct = (self.host, self.port,
                                         self.flow_info, self.scope_id)
            else:
                family = socket.AF_INET

        # Create socket
        self.socket = socket.socket(family, stream)
        if self.socket is None:
            # Log Error
            self.log.error("GraphiteHandler: Unable to create socket.")
            # Close Socket
            self._close()
            return
        # Enable keepalives?
        if self.proto != 'udp' and self.keepalive:
            self.log.error("GraphiteHandler: Setting socket keepalives...")
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE,
                                   self.keepaliveinterval)
            self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL,
                                   self.keepaliveinterval)
            self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 3)
        # Set socket timeout
        self.socket.settimeout(self.timeout)
        # Connect to graphite server
        try:
            self.socket.connect(connection_struct)
            # Log
            self.log.debug("GraphiteHandler: Established connection to "
                           "graphite server %s:%d.",
                           self.host, self.port)
        except Exception, ex:
            # Log Error
            self._throttle_error("GraphiteHandler: Failed to connect to "
                                 "%s:%i. %s.", self.host, self.port, ex)
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
