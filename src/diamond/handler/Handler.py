# coding=utf-8

import logging
import threading


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
