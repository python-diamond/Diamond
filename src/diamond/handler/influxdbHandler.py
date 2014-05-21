# coding=utf-8

"""
Send metrics to a [influxdb](https://github.com/influxdb/influxdb/) using the http interface.

v1.0 : creation
       Sebastien Prune THOMAS - prune@lecentre.net
       
- Dependency: 
    - influxdb client (pip install influxdb)
      you need version > 0.1.6 for HTTPS (not yet released)
      
- enable it in `diamond.conf` :

handlers = diamond.handler.influxdbHandler.InfluxdbHandler

- add config to `diamond.conf` :

[[InfluxdbHandler]]
host = localhost
port = 8086 #8084 for HTTPS
batch_size = 100 # default to 1
username = root
password = root
database = graphite

"""

import struct
from Handler import Handler

try:
    import influxdb
    from influxdb.client import InfluxDBClient
    InfluxDBClient
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
                           
        # Initialize Options
        self.ssl = self.config['ssl']
        self.hostname = self.config['hostname']
        self.port = int(self.config['port'])
        self.username = self.config['username']
        self.password = self.config['password']
        self.database = self.config['database']
        self.batch_size = int(self.config['batch_size'])
        self.max_backlog_multiplier = int(self.config['max_backlog_multiplier'])

        # Initialize Data
        self.batch = {}
        self.influx = None

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
            'batch_size': 'How many to store before sending to the influxdb server',
            'username': 'Username for connection',
            'password': 'Password for connection',
            'database': 'Database name',
            'max_backlog_multiplier': 'Number of metrics to keep in the pool (multiplied by batch size)',
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
            'max_backlog_multiplier': 1,
        })

        return config

    def __del__(self):
        """
        Destroy instance of the InfluxdbHandler class
        """
        self._close()

    def process(self, metric):
        # Add the data to the batch
        self.batch.setdefault(metric.path,[]).append([metric.timestamp, metric.value])

        # If there are sufficient metrics, then pickle and send
        if len(self.batch) >= self.batch_size:
            # Log
            self.log.debug("InfluxdbHandler: Sending batch size: %d",
                           self.batch_size)
            # Send pickled batch
            self._send()

    def _send(self):
        """
        Send data to Influxdb. Data that can not be sent will be kept in queued.
        """
        # Check to see if we have a valid socket. If not, try to connect.
        try:
            try:
                if self.influx is None:
                    self.log.debug("InfluxdbHandler: Socket is not connected. "
                                   "Reconnecting.")
                    self._connect()
                if self.influx is None:
                    self.log.debug("InfluxdbHandler: Reconnect failed.")
                else:
                    # build metrics data
                    metrics=[]
                    for path in self.batch:
                        metrics.append({"points": self.batch[path], "name": path, "columns": ["time","value"]})
                    # Send data to socket
                    self.influx.write_points(metrics)

                    # empty batch buffer
                    self.batch = {}
            except Exception:
                self._close()
                self._throttle_error("InfluxdbHandler: Error sending metrics.")
                raise
        finally:
            if len(self.batch) >= (
                    self.batch_size * self.max_backlog_multiplier):
                trim_offset = (self.batch_size
                               * self.trim_backlog_multiplier * -1)
                self.log.warn('InfluxdbHandler: Trimming backlog. Removing'
                              + ' oldest %d and keeping newest %d metrics',
                              len(self.batch) - abs(trim_offset),
                              abs(trim_offset))
                self.batch = self.batch[trim_offset:]


    def _connect(self):
        """
        Connect to the influxdb server
        """

        try:
          # Open Connection
          if influxdb.__version__ > "0.1.6":
              self.influx = InfluxDBClient(self.hostname, self.port, self.username, self.password, self.database, self.ssl)
          else:
              self.influx = InfluxDBClient(self.hostname, self.port, self.username, self.password, self.database)
              
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
