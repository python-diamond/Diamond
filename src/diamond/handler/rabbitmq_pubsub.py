# coding=utf-8

"""
Output the collected values to RabitMQ pub/sub channel
"""

from Handler import Handler
import pika
import sys

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
        self._bind()

    def _bind(self):
      """
         Create PUB socket and bind
      """
      self.connection=pika.BlockingConnection(pika.ConnectionParameters( host=self.server ) )
      self.channel = self.connection.channel()
      self.channel.exchange_declare(exchange=self.rmq_exchange, type='fanout')


    def __del__(self):
      """
        Destroy instance of the rmqHandler class
      """
      self.connection.close()

    def process(self, metric):
        """
          Process a metric and send it to zmq pub socket
        """
        # Acquire a lock
        self.lock.acquire()

        # Send the data as ......

        try:
          self.channel.basic_publish(exchange=self.rmq_exchange, routing_key='', body="%s" % metric )

        except Exception,e:  # Rough connection re-try logic.
          self.log.info("Failed to publishing to rabbitMQ. Attempting to reconnect.")
	  self._bind()

        # Release lock
        self.lock.release()

