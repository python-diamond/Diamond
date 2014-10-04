# coding=utf-8

"""
This is a meta handler to act as a shim for the new threading model. Please
do not try to use it as a normal handler
"""

from Handler import Handler


class QueueHandler(Handler):
    def __init__(self, config=None, queue=None, log=None):
        # Initialize Handler
        Handler.__init__(self, config=config, log=log)

        self.metrics = []
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
        self.metrics.append(metric)

    def flush(self):
        return self._flush()

    def _flush(self):
        """
        We skip any locking code due to the fact that this is now a single
        process per collector
        """
        if len(self.metrics) > 0:
            self.queue.put(self.metrics, block=False)
            self.metrics = []
