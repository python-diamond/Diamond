# coding=utf-8

"""
Send metrics to a [influxdb](https://github.com/influxdb/influxdb/) using the
http interface.

v1.0 : creation
v1.1 : force influxdb driver with SSL
v1.2 : added a timer to delay influxdb writing in case of failure
       this whill avoid the 100% cpu loop when influx in not responding
       Sebastien Prune THOMAS - prune@lecentre.net

- Dependency:
    - influxdb client (pip install influxdb)
      you need version > 0.1.6 for HTTPS (not yet released)

- enable it in `diamond.conf` :

handlers = diamond.handler.influxdbHandler.InfluxdbHandler

- add config to `diamond.conf` :

[[InfluxdbHandler]]
hostname = localhost
port = 8086 #8084 for HTTPS
batch_size = 100 # default to 1
cache_size = 1000 # default to 20000
username = root
password = root
database = graphite
time_precision = s
"""

import time
from Handler import Handler

try:
    from influxdb.client import InfluxDBClient
except ImportError:
    InfluxDBClient = None


class InfluxdbHandler(Handler):
    """
    Sending data to Influxdb using batched format
    """
    def __init__(self, config=None):
        """
        Create a new instance of the InfluxdbeHandler
        """
        # Initialize Handler
        Handler.__init__(self, config)

        if not InfluxDBClient:
            self.log.error('influxdb.client.InfluxDBClient import failed. '
                           'Handler disabled')
            self.enabled = False
            return

        # Initialize Options
        if self.config['ssl'] == "True":
            self.ssl = True
        else:
            self.ssl = False
        self.hostname = self.config['hostname']
        self.port = int(self.config['port'])
        self.username = self.config['username']
        self.password = self.config['password']
        self.database = self.config['database']
        self.batch_size = int(self.config['batch_size'])
        self.metric_max_cache = int(self.config['cache_size'])
        self.batch_count = 0
        self.time_precision = self.config['time_precision']

        # Initialize Data
        self.batch = {}
        self.influx = None
        self.batch_timestamp = time.time()
        self.time_multiplier = 1

        # Connect
        self._connect()

    def get_default_config_help(self):
        """
        Returns the help text for the configuration options for this handler
        """
        config = super(InfluxdbHandler, self).get_default_config_help()

        config.update({
            'hostname': 'Hostname',
            'port': 'Port',
            'ssl': 'set to True to use HTTPS instead of http',
            'batch_size': 'How many metrics to store before sending to the'
            ' influxdb server',
            'cache_size': 'How many values to store in cache in case of'
            ' influxdb failure',
            'username': 'Username for connection',
            'password': 'Password for connection',
            'database': 'Database name',
            'time_precision': 'time precision in second(s), milisecond(ms) or '
            'microsecond (u)',
        })

        return config

    def get_default_config(self):
        """
        Return the default config for the handler
        """
        config = super(InfluxdbHandler, self).get_default_config()

        config.update({
            'hostname': 'localhost',
            'port': 8086,
            'ssl': False,
            'username': 'root',
            'password': 'root',
            'database': 'graphite',
            'batch_size': 1,
            'cache_size': 20000,
            'time_precision': 's',
        })

        return config

    def __del__(self):
        """
        Destroy instance of the InfluxdbHandler class
        """
        self._close()

    def process(self, metric):
        if self.batch_count <= self.metric_max_cache:
            # Add the data to the batch
            self.batch.setdefault(metric.path, []).append([metric.timestamp,
                                                           metric.value])
            self.batch_count += 1
        # If there are sufficient metrics, then pickle and send
        if self.batch_count >= self.batch_size and (
                time.time() - self.batch_timestamp) > 2**self.time_multiplier:
            # Log
            self.log.debug(
                "InfluxdbHandler: Sending batch sizeof : %d/%d after %fs",
                self.batch_count,
                self.batch_size,
                (time.time() - self.batch_timestamp))
            # reset the batch timer
            self.batch_timestamp = time.time()
            # Send pickled batch
            self._send()
        else:
            self.log.debug(
                "InfluxdbHandler: not sending batch of %d as timestamp is %f",
                self.batch_count,
                (time.time() - self.batch_timestamp))

    def _send(self):
        """
        Send data to Influxdb. Data that can not be sent will be kept in queued.
        """
        # Check to see if we have a valid socket. If not, try to connect.
        try:
                if self.influx is None:
                    self.log.debug("InfluxdbHandler: Socket is not connected. "
                                   "Reconnecting.")
                    self._connect()
                if self.influx is None:
                    self.log.debug("InfluxdbHandler: Reconnect failed.")
                else:
                    # build metrics data
                    metrics = []
                    for path in self.batch:
                        metrics.append({
                            "points": self.batch[path],
                            "name": path,
                            "columns": ["time", "value"]})
                    # Send data to influxdb
                    self.log.debug("InfluxdbHandler: writing %d series of data",
                                   len(metrics))
                    self.influx.write_points(metrics,
                                             time_precision=self.time_precision)

                    # empty batch buffer
                    self.batch = {}
                    self.batch_count = 0
                    self.time_multiplier = 1

        except Exception:
                self._close()
                if self.time_multiplier < 5:
                    self.time_multiplier += 1
                self._throttle_error(
                    "InfluxdbHandler: Error sending metrics, waiting for %ds.",
                    2**self.time_multiplier)
                raise

    def _connect(self):
        """
        Connect to the influxdb server
        """

        try:
            # Open Connection
            self.influx = InfluxDBClient(self.hostname, self.port,
                                         self.username, self.password,
                                         self.database, self.ssl)
            # Log
            self.log.debug("InfluxdbHandler: Established connection to "
                           "%s:%d/%s.",
                           self.hostname, self.port, self.database)
        except Exception, ex:
            # Log Error
            self._throttle_error("InfluxdbHandler: Failed to connect to "
                                 "%s:%d/%s. %s",
                                 self.hostname, self.port, self.database, ex)
            # Close Socket
            self._close()
            return

    def _close(self):
        """
        Close the socket = do nothing for influx which is http stateless
        """
        self.influx = None
