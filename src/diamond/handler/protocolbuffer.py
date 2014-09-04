# coding=utf-8

"""
Send metrics to a [graphite](http://graphite.wikidot.com/) using the high
performace protocol buffer interface.

Graphite is an enterprise-scale monitoring tool that runs well on cheap
hardware. It was originally designed and written by Chris Davis at Orbitz in
2006 as side project that ultimately grew to be a foundational monitoring tool.
In 2008, Orbitz allowed Graphite to be released under the open source Apache
2.0 license. Since then Chris has continued to work on Graphite and has
deployed it at other companies including Sears, where it serves as a pillar of
the e-commerce monitoring system. Today many
[large companies](http://graphite.readthedocs.org/en/latest/who-is-using.html)
use it.

- enable it in `diamond.conf` :

`    handlers = diamond.handler.protocolbuffer.ProtocolBufferHandler
`

"""
from struct import pack as struct_pack

from graphite import GraphiteHandler
from zlib import compress

try:
    from diamond.handler.proto_handler_pb2 import Metric
except Exception:
    raise ValueError("Cannot import protocol buffer library successfully")

class ProtocolBufferHandler(GraphiteHandler):
    """
    Overrides the GraphiteHandler class
    Sending data to graphite using batched protocol buffer format
    """
    def __init__(self, config=None):
        """
        Create a new instance of the ProtocolBufferHandler
        """
        # Initialize GraphiteHandler
        GraphiteHandler.__init__(self, config)
        # Initialize Data
        self.batch = ""
        self.metrics = ""
        self.metric_count = 0
        # Initialize Options
        self.batch_size = int(self.config['batch'])
        if self.config['compressed'] == 'True':
            self.compress = True
        else:
            self.compress = False
        self.delimiter = str(self.config['delimiter'])

    def get_default_config_help(self):
        """
        Returns the help text for the configuration options for this handler
        """
        config = super(ProtocolBufferHandler, self).get_default_config_help()

        config.update({
        })

        return config

    def get_default_config(self):
        """
        Return the default config for the handler
        """
        config = super(ProtocolBufferHandler, self).get_default_config()

        config.update({
        })

        return config

    def process(self, metric):
        # Convert metric to protocol buffer format
        m = Metric()
        m.path = metric.path
        m.timestamp = metric.timestamp
        m.value = metric.value
        # Add the metric to the batch
        self.batch += m.SerializeToString() + self.delimiter
        self.metric_count += 1
        del m
        # If there are sufficient metrics, then pickle and send
        if self.metric_count >= self.batch_size:
            self.batch = self.batch[:-len(self.delimiter)]
            self.log.debug("ProtocolBufferHandler: Sending %d metrics",
                           " of size %d" % (self.metric_count, len(self.batch)))
            if self.compress: 
                self.metrics = compress(self.batch)
                self.log.debug("ProtocolBufferHandler: ","
                               compressed %d" % len(self.metrics))
            else:
                self.metrics = self.batch

            #for some reason, twisted appends four characters to protobuf messages in carbon
            #we need to pack on four characters to emulate that
            self.metrics = "aaaa" + self.metrics

            # Send batch
            self._send()
            # Flush the metric pack down the wire
            self.flush()
            # Clear Batch
            self.batch = ""
            self.metric_count = 0

    def _send(self):
        """
        Send data to graphite. Data that can not be sent will be queued.
        """
        # Check to see if we have a valid socket. If not, try to connect.
        try:
            if self.socket is None:
                self.log.debug("ProtocolBufferHandler: Socket is not connected. "
                               "Reconnecting.")
                self._connect()
            if self.socket is None:
                self.log.debug("ProtocolBufferHandler: Reconnect failed.")
            else:
                # Send data to socket
                self._send_data(self.metrics)
                self.metrics = ""
        except Exception:
            self._close()
            self._throttle_error("ProtocolBufferHandler: Error sending metrics.")
            raise
