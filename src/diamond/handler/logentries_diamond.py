# coding=utf-8
"""
[Logentries: Log Management & Analytics Made Easy ](https://logentries.com/).
Send Diamond stats to your Logentries Account where you can monitor and alert
based on data in real time.

#### Dependencies


#### Configuration

Enable this handler

 * handers = diamond.handler.logentries.LogentriesDiamondHandler
 * log_token = [Your Log Token](https://logentries.com/doc/input-token/)


"""

from Handler import Handler
import logging
import time
import urllib2
import json


class LogentriesDiamondHandler(Handler):
    """
      Implements the abstract Handler class
    """
    def __init__(self, config=None):
        """
        New instance of LogentriesDiamondHandler class
        """

        Handler.__init__(self, config)
        self.log_token = self.config.get('log_token', None)
        if self.log_token is None:
            raise Exception

    def get_default_config_help(self):
        """
        Help text
        """
        config = super(LogentriesDiamondHandler,
                       self).get_default_config_help()

        config.update({
            'log_token': None,
        })

        return config

    def get_default_config(self):
        """
        Return default config for the handler
        """
        config = super(LogentriesDiamondHandler, self).get_default_config()

        config.update({
            'log_token': None,
        })

        return config

    def process(self, metric):
        """
        Process metric by sending it to datadog api
        """

        time.sleep(1)
        self._send(metric)

    def _send(self, metric):
        """
        Convert message to a json object and send to Lognetries
        """
        logging.debug("Sending logs.")
        topic, value, timestamp = str(metric).split()
        msg = json.dumps({"event": {topic: value}})
        req = urllib2.Request("https://js.logentries.com/v1/logs/"
                              + self.log_token, msg)
        urllib2.urlopen(req)
        time.sleep(1)
