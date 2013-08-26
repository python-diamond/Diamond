# coding=utf-8

"""
Output the collected values to RabitMQ pub/sub channel
"""

from Handler import Handler
import pika


class rmqHandler (Handler):
    """
      Implements the abstract Handler class
      Sending data to a RabbitMQ pub/sub channel
    """

    def __init__(self, config=None):
        """
          Create a new instance of rmqHandler class
        """

        # Initialize Handler
        Handler.__init__(self, config)

        # Initialize Data
        self.connection = None
        self.channel = None

        # Initialize Options
        self.server = self.config['server']
        self.rmq_exchange = self.config['rmq_exchange']

        # Create rabbitMQ pub socket and bind
        try:
            self._bind()
        except pika.exceptions.AMQPConnectionError:
            self.log.error('Failed to bind to rabbitMQ pub socket')

    def get_default_config_help(self):
        """
        Returns the help text for the configuration options for this handler
        """
        config = super(rmqHandler, self).get_default_config_help()

        config.update({
            'server': '',
            'rmq_exchange': '',
        })

        return config

    def get_default_config(self):
        """
        Return the default config for the handler
        """
        config = super(rmqHandler, self).get_default_config()

        config.update({
            'server': '127.0.0.1',
            'rmq_exchange': 'diamond',
        })

        return config

    def _bind(self):
        """
           Create PUB socket and bind
        """
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=self.server))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=self.rmq_exchange, type='fanout')

    def __del__(self):
        """
          Destroy instance of the rmqHandler class
        """
        try:
            self.connection.close()
        except AttributeError:
            pass

    def process(self, metric):
        """
          Process a metric and send it to zmq pub socket
        """
        # Send the data as ......

        try:
            self.channel.basic_publish(exchange=self.rmq_exchange,
                                       routing_key='', body="%s" % metric)

        except Exception:  # Rough connection re-try logic.
            self.log.info("Failed publishing to rabbitMQ. Attempting reconnect")
        self._bind()
