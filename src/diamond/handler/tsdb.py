# coding=utf-8

"""
Send metrics to a [OpenTSDB](http://opentsdb.net/) server.

[OpenTSDB](http://opentsdb.net/) is a distributed, scalable Time Series
Database (TSDB) written on top of [HBase](http://hbase.org/). OpenTSDB was
written to address a common need: store, index and serve metrics collected from
computer systems (network gear, operating systems, applications) at a large
scale, and make this data easily accessible and graphable.

Thanks to HBase's scalability, OpenTSDB allows you to collect many thousands of
metrics from thousands of hosts and applications, at a high rate (every few
seconds). OpenTSDB will never delete or downsample data and can easily store
billions of data points. As a matter of fact, StumbleUpon uses it to keep track
of hundred of thousands of time series and collects over 1 billion data points
per day in their main production datacenter.

Imagine having the ability to quickly plot a graph showing the number of DELETE
statements going to your MySQL database along with the number of slow queries
and temporary files created, and correlate this with the 99th percentile of
your service's latency. OpenTSDB makes generating such graphs on the fly a
trivial operation, while manipulating millions of data point for very fine
grained, real-time monitoring.

One of the key features of OpenTSDB is working with tags. When collecting the
same information for multiple instances (let's say the CPU or the number of
bytes received on an interface), OpenTSDB uses the same metric name and a
variable number of tags to identify what you were collecting. See
http://opentsdb.net/docs/build/html/user_guide/query/timeseries.html for more
information.

The system per default adds a tag 'hostname' with the hostname where the
collection took place. You can add as many as you like. The 'tags' config
element allows for both comma-separated or space separated key value pairs.

Example :
tags = environment=test,datacenter=north

==== Notes

We don't automatically make the metrics via mkmetric, so we recommand you run
with the null handler and log the output and extract the key values to mkmetric
yourself.

- enable it in `diamond.conf` :

`    handlers = diamond.handler.tsdb.TSDBHandler
`
'
"""

from Handler import Handler
import socket


class TSDBHandler(Handler):
    """
    Implements the abstract Handler class, sending data to OpenTSDB
    """
    RETRY = 3

    def __init__(self, config=None):
        """
        Create a new instance of the TSDBHandler class
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
        self.tags = ""
        if isinstance(self.config['tags'], basestring):
            self.tags = self.config['tags']
        elif isinstance(self.config['tags'], list):
            for tag in self.config['tags']:
                self.tags += " "+tag
        if not(self.tags == "") and not(self.tags.startswith(' ')):
            self.tags = " "+self.tags

        # OpenTSDB refuses tags with = in the value, so see whether we have
        # some of them in it..
        for tag in self.tags.split(" "):
            if tag.count('=') > 1:
                raise Exception("Invalid tag name "+tag)
        # Connect
        self._connect()

    def get_default_config_help(self):
        """
        Returns the help text for the configuration options for this handler
        """
        config = super(TSDBHandler, self).get_default_config_help()

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
        config = super(TSDBHandler, self).get_default_config()

        config.update({
            'host': '',
            'port': 1234,
            'timeout': 5,
            'format': '{Collector}.{Metric} {timestamp} {value} hostname={host}'
                      '{tags}',
            'tags': '',
        })

        return config

    def __del__(self):
        """
        Destroy instance of the TSDBHandler class
        """
        self._close()

    def process(self, metric):
        """
        Process a metric by sending it to TSDB
        """

        metric_str = self.metric_format.format(
            Collector=metric.getCollectorPath(),
            Path=metric.path,
            Metric=metric.getMetricPath(),
            host=metric.host,
            timestamp=metric.timestamp,
            value=metric.value,
            tags=self.tags
        )
        # Just send the data as a string
        self._send("put " + str(metric_str) + "\n")

    def _send(self, data):
        """
        Send data to TSDB. Data that can not be sent will be queued.
        """
        retry = self.RETRY
        # Attempt to send any data in the queue
        while retry > 0:
            # Check socket
            if not self.socket:
                # Log Error
                self.log.error("TSDBHandler: Socket unavailable.")
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
                self.log.error("TSDBHandler: Failed sending data. %s.", e)
                # Attempt to restablish connection
                self._close()
                # Decrement retry
                retry -= 1
                # try again
                continue

    def _connect(self):
        """
        Connect to the TSDB server
        """
        # Create socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if socket is None:
            # Log Error
            self.log.error("TSDBHandler: Unable to create socket.")
            # Close Socket
            self._close()
            return
        # Set socket timeout
        self.socket.settimeout(self.timeout)
        # Connect to graphite server
        try:
            self.socket.connect((self.host, self.port))
            # Log
            self.log.debug("Established connection to TSDB server %s:%d",
                           self.host, self.port)
        except Exception, ex:
            # Log Error
            self.log.error("TSDBHandler: Failed to connect to %s:%i. %s",
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
