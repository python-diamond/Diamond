# coding=utf-8

"""
[Librato](http://librato.com) is an infrastructure software as a service company
dedicated to delivering beautiful, easy to use tools that make managing your
operations more fun and efficient.

#### Dependencies

 * [librato-metrics](https://github.com/librato/python-librato)

#### Configuration

Enable this handler

 * handers = diamond.handler.librato.LibratoHandler

 * user = LIBRATO_USERNAME
 * apikey = LIBRATO_API_KEY

"""

from Handler import Handler
import logging
import librato

class LibratoHandler(Handler):

    def __init__(self, config=None):
        """
        Create a new instance of the LibratoHandler class
        """
        # Initialize Handler
        Handler.__init__(self, config)
        logging.debug("Initialized statsd handler.")
        # Initialize Options
        api                         = librato.connect(self.conf['user'],
                                                      self.conf['apikey'])
        self.queue                  = api.new_queue()
        self.batch_size             = 300
        self.current_n_measurements = 0

    def process(self, metric):
        """
        Process a metric by sending it to Librato
        """
        path = metric.getCollectorPath()
        path += '.'
        path += metric.getMetricPath()

        if metric.metric_type == 'GAUGE':
            m_type = 'gauge'
        else:
            m_type = 'counter'
        self.queue.add(path,                # name
                       float(metric.value), # value
                       type=m_type,
                       source=metric.host,
                       measure_time=metric.timestamp)
        self.current_n_measurements += 1

        if current_n_measurements >= self.batch_size:
            self.log.debug("LibratoHandler: Sending batch size: %d",
                            self.current_n_measurements)
            self._send()

    def _send(self):
        """
        Send data to Librato.
        """
        self.queue.submit()
        self.current_n_measurements = 0
