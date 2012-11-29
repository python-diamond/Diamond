# coding=utf-8

"""
Output the collected values to a Zer0MQ pub/sub channel
"""

from Handler import Handler

import zmq


class zmqHandler (Handler):
    """
      Implements the abstract Handler class
      Sending data to a Zer0MQ pub channel
    """

    def __init__(self, config=None):

        """
          Create a new instance of zmqHandler class
        """

        # Initialize Handler
        Handler.__init__(self, config)

        # Initialize Data
        self.context = None

        self.socket = None

        # Initialize Options
        self.port = int(self.config['port'])

        # Create ZMQ pub socket and bind
        self._bind()

    def _bind(self):
        """
           Create PUB socket and bind
        """
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind("tcp://*:%i" % self.port)

    def __del__(self):
        """
          Destroy instance of the zmqHandler class
        """
        pass

    def process(self, metric):
        """
          Process a metric and send it to zmq pub socket
        """

        # Send the data as ......
        self.socket.send("%s" % str(metric))
