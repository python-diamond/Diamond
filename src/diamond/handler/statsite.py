# coding=utf-8

"""
Send metrics to a [Statsite](https://github.com/armon/statsite/)
using the default interface.

Statsite
========

This is a stats aggregation server. Statsite is based heavily
on Etsy's [StatsD](https://github.com/etsy/statsd). This is
a re-implementation of the Python version of
[statsite](https://github.com/kiip/statsite).

Features
--------

* Basic key/value metrics
* Send timer data, statsite will calculate:
  - Mean
  - Min/Max
  - Standard deviation
  - Median, Percentile 95, Percentile 99
* Send counters that statsite will aggregate


Architecture
-------------

Statsite is designed to be both highly performant,
and very flexible. To achieve this, it implements the stats
collection and aggregation in pure C, using libev to be
extremely fast. This allows it to handle hundreds of connections,
and millions of metrics. After each flush interval expires,
statsite performs a fork/exec to start a new stream handler
invoking a specified application. Statsite then streams the
aggregated metrics over stdin to the application, which is
free to handle the metrics as it sees fit.

This allows statsite to aggregate metrics and then ship metrics
to any number of sinks (Graphite, SQL databases, etc). There
is an included Python script that ships metrics to graphite.

Additionally, statsite tries to minimize memory usage by not
storing all the metrics that are received. Counter values are
aggregated as they are received, and timer values are stored
and aggregated using the Cormode-Muthurkrishnan algorithm from
"Effective Computation of Biased Quantiles over Data Streams".
This means that the percentile values are not perfectly accurate,
and are subject to a specifiable error epsilon. This allows us to
store only a fraction of the samples.

"""

from Handler import Handler
import socket


class StatsiteHandler(Handler):
    """
    Implements the abstract Handler class, sending data to statsite
    """
    RETRY = 3

    def __init__(self, config=None):
        """
        Create a new instance of the StatsiteHandler class
        """
        # Initialize Handler
        Handler.__init__(self, config)

        # Initialize Data
        self.socket = None

        # Initialize Options
        self.host = self.config['host']
        self.tcpport = int(self.config['tcpport'])
        self.udpport = int(self.config['udpport'])
        self.timeout = int(self.config['timeout'])

        # Connect
        self._connect()

    def get_default_config_help(self):
        """
        Returns the help text for the configuration options for this handler
        """
        config = super(StatsiteHandler, self).get_default_config_help()

        config.update({
            'host': '',
            'tcpport': '',
            'udpport': '',
            'timeout': '',
        })

        return config

    def get_default_config(self):
        """
        Return the default config for the handler
        """
        config = super(StatsiteHandler, self).get_default_config()

        config.update({
            'host': '',
            'tcpport': 1234,
            'udpport': 1234,
            'timeout': 5,
        })

        return config

    def __del__(self):
        """
        Destroy instance of the StatsiteHandler class
        """
        self._close()

    def process(self, metric):
        """
        Process a metric by sending it to statsite
        """
        # Just send the data as a string
        self._send(str(metric))

    def _send(self, data):
        """
        Send data to statsite. Data that can not be sent will be queued.
        """
        retry = self.RETRY
        # Attempt to send any data in the queue
        while retry > 0:
            # Check socket
            if not self.socket:
                # Log Error
                self.log.error("StatsiteHandler: Socket unavailable.")
                # Attempt to restablish connection
                self._connect()
                # Decrement retry
                retry -= 1
                # Try again
                continue
            try:
                # Send data to socket
                data = data.split()
                data = data[0] + ":" + data[1] + "|kv\n"
                self.socket.sendall(data)
                # Done
                break
            except socket.error, e:
                # Log Error
                self.log.error("StatsiteHandler: Failed sending data. %s.", e)
                # Attempt to restablish connection
                self._close()
                # Decrement retry
                retry -= 1
                # try again
                continue

    def _connect(self):
        """
        Connect to the statsite server
        """
        # Create socket
        if self.udpport > 0:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.port = self.udpport
        elif self.tcpport > 0:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.port = self.tcpport
        if socket is None:
            # Log Error
            self.log.error("StatsiteHandler: Unable to create socket.")
            # Close Socket
            self._close()
            return
        # Set socket timeout
        self.socket.settimeout(self.timeout)
        # Connect to statsite server
        try:
            self.socket.connect((self.host, self.port))
            # Log
            self.log.debug("Established connection to statsite server %s:%d",
                           self.host, self.port)
        except Exception, ex:
            # Log Error
            self.log.error("StatsiteHandler: Failed to connect to %s:%i. %s",
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
