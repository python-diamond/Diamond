# coding=utf-8

import logging
import threading
import traceback
from configobj import ConfigObj


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

        # Initialize Blank Configs
        self.config = ConfigObj()

        # Load default
        self.config.merge(self.get_default_config())

        # Load in user
        self.config.merge(config)

        # Initialize Lock
        self.lock = threading.Lock()

    def get_default_config_help(self):
        """
        Returns the help text for the configuration options for this handler
        """
        return {
            'get_default_config_help': 'get_default_config_help',
        }

    def get_default_config(self):
        """
        Return the default config for the handler
        """
        return {
            'get_default_config': 'get_default_config',
        }

    def _process(self, metric):
        """
        Decorator for processing handlers with a lock, catching exceptions
        """
        try:
            try:
                self.lock.acquire()
                self.process(metric)
            except Exception:
                self.log.error(traceback.format_exc())
        finally:
            if self.lock.locked():
                self.lock.release()

    def process(self, metric):
        """
        Process a metric

        Should be overridden in subclasses
        """
        raise NotImplementedError

    def _flush(self):
        """
        Decorator for flushing handlers with an lock, catching exceptions
        """
        try:
            try:
                self.lock.acquire()
                self.flush()
            except Exception:
                self.log.error(traceback.format_exc())
        finally:
            if self.lock.locked():
                self.lock.release()

    def flush(self):
        """
        Flush metrics

        Optional: Should be overridden in subclasses
        """
        pass
