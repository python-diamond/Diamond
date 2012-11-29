# coding=utf-8

import logging
import threading
import traceback


class Handler(object):
    """
    Handlers process metrics that are collected by Collectors.
    """
    def __init__(self, config=None):
        """
        Create a new instance of the Handler class
        """
        # Initialize Log
        self.log = logging.getLogger('diamond')
        # Initialize Data
        self.config = config
        # Initialize Lock
        self.lock = threading.Condition(threading.Lock())

    def _process(self, metric):
        """
        Decorator for processing handlers with a lock, catching exceptions
        """
        try:
            self.log.debug("Running Handler %s locked" % (self))
            with self.lock:
                self.process(metric)
        except Exception:
                self.log.error(traceback.format_exc())
        finally:
            self.log.debug("Unlocked Handler %s" % (self))

    def process(self, metric):
        """
        Process a metric

        Should be overridden in subclasses
        """
        raise NotImplementedError

    def flush(self):
        """
        Flush metrics

        Optional: Should be overridden in subclasses
        """
        pass
