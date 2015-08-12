# coding=utf-8

"""
Send metrics to a HTTP(S) endpoint encoded serialized via protocol buffers

v0.1 : first draft

- Dependency:
    - google protobuf (pip install protobuf)

- enable it in `diamond.conf` :

handlers = diamond.handler.protobufHandler.ProtobufHandler

- add config to `diamond.conf` :

[[ProtobufHandler]]
url = localhost
batch_size = 100 # default to 1
max_cache = 50000 # default to 10000
"""

import urllib2
import contextlib

from time import time
from Handler import Handler

try:
    from diamond.utils.metric_pb2 import MetricBatch
except ImportError:
    MetricBatch = None


class ProtobufHandler(Handler):
    """
    Sending data to HTTP(S) endpoint using protobuf encoded content
    """
    def __init__(self, config=None):
        # Initialize Handler
        Handler.__init__(self, config)

        # Do we have the protobuf library
        if not MetricBatch:
            self.log.error('ProtobufHandler: protobuf import failed - handler disabled')
            self.enabled = False
            return

        self.url = self.config['url']
        self.batch_size = int(self.config['batch_size'])
        self.max_cache = int(self.config['max_cache'])

        # Sanity Check
        if self.max_cache < self.batch_size:
            self.log.error('ProtobufHandler: max_cache < batch_size - handler disabled')
            self.enabled = False
            return

        # Initialize Throttle Timer
        self.send_throttle_wait = 10
        self.send_throttle_timestamp = 0

        # Initialize Batch Buffer
        self.batch = []

    def get_default_config_help(self):
        """
        Returns the help text for the configuration options for this handler
        """
        config = super(ProtobufHandler, self).get_default_config_help()

        config.update({
            'url': 'full url to http(s) endpoint',
            'batch_size': 'How many metrics to store before sending them',
            'max_cache': 'Maximum metrics to hold in memory in case of endpoint failure'
        })

        return config

    def get_default_config(self):
        """
        Return the default config for the handler
        """
        config = super(ProtobufHandler, self).get_default_config()

        config.update({
            'url': 'http://localhost/',
            'batch_size': 1,
            'max_cache': 10000
        })

        return config

    def __del__(self):
        self._close()

    def process(self, metric):
        throttled = (
            self.send_throttle_timestamp > 0 and 
            time() < self.send_throttle_timestamp + self.send_throttle_wait
        )

        # Take care of the cache limit
        if len(self.batch) < self.max_cache:
            self.batch.append(metric)
        else:
            self.log.debug('ProtobufHandler: max_cache exceeded - discarding metric')

        # If there are sufficient metrics, then pickle and send
        if len(self.batch) >= self.batch_size and not throttled:
            self.log.debug(
                "ProtobufHandler: Sending batch sizeof : %d/%d",
                len(self.batch),
                self.batch_size
            )
            # Send pickled batch
            self._send()
        else:
            self.log.debug(
                "ProtobufHandler: not sending batch of %d (throttdled: %s)", 
                len(self.batch),
                str(throttled)
            )

    def _send(self):
        try:
            # build metricbatch protocol buffer
            metricbatch = MetricBatch()
            for metric in self.batch:
                buf = metricbatch.metric.add()
                buf.path = metric.path
                buf.value = metric.value
                buf.timestamp = metric.timestamp
                buf.precision = metric.precision
                buf.host = metric.host
                buf.ttl = metric.ttl

            # Send data to http(s) endpoint
            self.log.debug("ProtobufHandler: sending %d metrics", len(self.batch))
            req = urllib2.Request(
                url=self.url, 
                data=metricbatch.SerializeToString(),
                headers={
                    'Content-Type': 'application/x-protobuf',
                    # TODO: set this to x-protobuf as well
                    'Accept': 'application/json'
                }
            )

            with contextlib.closing(urllib2.urlopen(req)) as fh:
                fh.read()

            # empty batch buffer
            self.batch = []
            self.batch_count = 0

        except Exception as err:
            self._throttle_error(
                "ProtobufHandler: error sending metrics, not sending for %ds (%s)",
                self.send_throttle_wait,
                str(err)
            )
            self.send_throttle_timestamp = time()
            self._close()
        else:
            self.send_throttle_timestamp = 0

    def _close(self):
        """
        Close the socket = do nothing since http is stateless
        """
        pass
