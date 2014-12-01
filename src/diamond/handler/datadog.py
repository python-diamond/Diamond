"""
[Datadog](http://www.datadoghq.com/) is a monitoring service for IT,
Operations and Development teams who write and run applications
at scale, and want to turn the massive amounts of data produced
by their apps, tools and services into actionable insight.

#### Dependencies

  * [dogapi]

#### Configuration

Enable handler

  * handlers = diamond.handler.datadog.DatadogHandler,

  * api_key = DATADOG_API_KEY

  * queue_size = [optional | 1]

"""

from Handler import Handler
import logging
from collections import deque

try:
    import dogapi
except ImportError:
    dogapi = None


class DatadogHandler(Handler):

    def __init__(self, config=None):
        """
        New instance of DatadogHandler class
        """

        Handler.__init__(self, config)
        logging.debug("Initialized Datadog handler.")

        if dogapi is None:
            logging.error("Failed to load dogapi module.")
            return

        self.api = dogapi.dog_http_api
        self.api.api_key = self.config.get('api_key', '')
        self.queue_size = self.config.get('queue_size', 1)
        self.queue = deque([])

    def get_default_config_help(self):
        """
        Help text
        """
        config = super(DatadogHandler, self).get_default_config_help()

        config.update({
            'api_key': '',
            'queue_size': '',
        })

        return config

    def get_default_config(self):
        """
        Return default config for the handler
        """
        config = super(DatadogHandler, self).get_default_config()

        config.update({
            'api_key': '',
            'queue_size': '',
        })

        return config

    def process(self, metric):
        """
        Process metric by sending it to datadog api
        """

        self.queue.append(metric)
        if len(self.queue) >= self.queue_size:
            self._send()

    def flush(self):
        """
        Flush metrics
        """

        self._send()

    def _send(self):
        """
        Take metrics from queue and send it to Datadog API
        """

        while len(self.queue) > 0:
            metric = self.queue.popleft()

            path = '%s.%s.%s' % (
                metric.getPathPrefix(),
                metric.getCollectorPath(),
                metric.getMetricPath()
            )

            topic, value, timestamp = str(metric).split()
            logging.debug(
                "Sending.. topic[%s], value[%s], timestamp[%s]",
                path,
                value,
                timestamp
            )

            self.api.metric(path, (timestamp, value), host=metric.host)
