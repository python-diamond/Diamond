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

 * queue_size = Integer value


"""

from Handler import Handler
import logging
import urllib2
import json
from collections import deque


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
        self.queue_size = int(self.config['queue_size'])
        self.queue = deque([])
        if self.log_token is None:
            raise Exception

    def get_default_config_help(self):
        """
        Help text
        """
        config = super(LogentriesDiamondHandler,
                       self).get_default_config_help()

        config.update({
            'log_token': '',
            'queue_size': ''
        })

        return config

    def get_default_config(self):
        """
        Return default config for the handler
        """
        config = super(LogentriesDiamondHandler, self).get_default_config()

        config.update({
            'log_token': '',
            'queue_size': 100
        })

        return config

    def process(self, metric):
        """
        Process metric by sending it to datadog api
        """

        self.queue.append(metric)
        if len(self.queue) >= self.queue_size:
            logging.debug("Queue is full, sending logs to Logentries")
            self._send()

    def _send(self):
        """
        Convert message to a json object and send to Lognetries
        """
        while len(self.queue) > 0:
            metric = self.queue.popleft()
            topic, value, timestamp = str(metric).split()
            msg = json.dumps({"event": {topic: value}})
            req = urllib2.Request("https://js.logentries.com/v1/logs/" +
                                  self.log_token, msg)
            try:
                urllib2.urlopen(req)
            except urllib2.URLError, e:
                logging.error("Can't send log message to Logentries %s", e)
