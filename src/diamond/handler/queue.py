# coding=utf-8

"""
This is a meta handler to act as a shim for the new threading model. Please
do not try to use it as a normal handler
"""

from Handler import Handler
import Queue


class QueueHandler(Handler):

    def __init__(self, config=None, queue=None, log=None):
        # Initialize Handler
        Handler.__init__(self, config=config, log=log)

        self.queue = queue

    def __del__(self):
        """
        Ensure as many of the metrics as possible are sent to the handers on
        a shutdown
        """
        self._flush()

    def process(self, metric):
        return self._process(metric)

    def _process(self, metric):
        """
        We skip any locking code due to the fact that this is now a single
        process per collector
        """
        try:
            self.queue.put(metric, block=False)
        except Queue.Full:
            self._throttle_error('Queue full, check handlers for delays')

    def flush(self):
        return self._flush()

    def _flush(self):
        """
        We skip any locking code due to the fact that this is now a single
        process per collector
        """
        # Send a None down the queue to indicate a flush
        try:
            self.queue.put(None, block=False)
        except Queue.Full:
            self._throttle_error('Queue full, check handlers for delays')
