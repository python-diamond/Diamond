# coding=utf-8

import logging
import threading
import traceback
from configobj import ConfigObj
import time


class Handler(object):
    """
    Handlers process metrics that are collected by Collectors.
    """
    def __init__(self, config=None, log=None):
        """
        Create a new instance of the Handler class
        """

        # Enabled? Default to yes, but allow handlers to disable themselves
        self.enabled = True

        # Initialize Log
        if log is None:
            self.log = logging.getLogger('diamond')
        else:
            self.log = log

        # Initialize Blank Configs
        self.config = ConfigObj()

        # Load default
        self.config.merge(self.get_default_config())

        # Load in user
        self.config.merge(config)

        # error logging throttling
        self.server_error_interval = float(self.config['server_error_interval'])
        self._errors = {}

        # Initialize Lock
        self.lock = threading.Lock()

    def get_default_config_help(self):
        """
        Returns the help text for the configuration options for this handler
        """
        return {
            'get_default_config_help': 'get_default_config_help',
            'server_error_interval': ('How frequently to send repeated server '
                                      'errors'),
        }

    def get_default_config(self):
        """
        Return the default config for the handler
        """
        return {
            'get_default_config': 'get_default_config',
            'server_error_interval': 120,
        }

    def _process(self, metric):
        """
        Decorator for processing handlers with a lock, catching exceptions
        """
        if not self.enabled:
            return
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
        if not self.enabled:
            return
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

    def _throttle_error(self, msg, *args, **kwargs):
        """
        Avoids sending errors repeatedly. Waits at least
        `self.server_error_interval` seconds before sending the same error
        string to the error logging facility. If not enough time has passed,
        it calls `log.debug` instead

        Receives the same parameters as `Logger.error` an passes them on to the
        selected logging function, but ignores all parameters but the main
        message string when checking the last emission time.

        :returns: the return value of `Logger.debug` or `Logger.error`
        """
        now = time.time()
        if msg in self._errors:
            if ((now - self._errors[msg]) >=
                    self.server_error_interval):
                fn = self.log.error
                self._errors[msg] = now
            else:
                fn = self.log.debug
        else:
            self._errors[msg] = now
            fn = self.log.error

        return fn(msg, *args, **kwargs)

    def _reset_errors(self, msg=None):
        """
        Resets the logging throttle cache, so the next error is emitted
        regardless of the value in `self.server_error_interval`

        :param msg: if present, only this key is reset. Otherwise, the whole
            cache is cleaned.
        """
        if msg is not None and msg in self._errors:
            del self._errors[msg]
        else:
            self._errors = {}
