# coding=utf-8

"""
Output the collected values to RabitMQ pub/sub channel
"""

from Handler import Handler
import time

try:
    import pika
except ImportError:
    pika = None


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

        if pika is None:
            self.log.error('pika import failed. Handler disabled')
            self.enabled = False
            return

        # Initialize Data
        self.connections = {}
        self.channels = {}
        self.reconnect_interval = 1

        # Initialize Options
        tmp_rmq_server = self.config['rmq_server']
        if type(tmp_rmq_server) is list:
            self.rmq_server = tmp_rmq_server
        else:
            self.rmq_server = [tmp_rmq_server]

        self.rmq_port = 5672
        self.rmq_exchange = self.config['rmq_exchange']
        self.rmq_user = None
        self.rmq_password = None
        self.rmq_vhost = '/'
        self.rmq_exchange_type = 'fanout'
        self.rmq_durable = True
        self.rmq_heartbeat_interval = 300

        self.get_config()
        # Create rabbitMQ pub socket and bind
        try:
            self._bind_all()
        except pika.exceptions.AMQPConnectionError:
            self.log.error('Failed to bind to rabbitMQ pub socket')

    def get_config(self):
        """ Get and set config options from config file """
        if 'rmq_port' in self.config:
            self.rmq_port = int(self.config['rmq_port'])

        if 'rmq_user' in self.config:
            self.rmq_user = self.config['rmq_user']

        if 'rmq_password' in self.config:
            self.rmq_password = self.config['rmq_password']

        if 'rmq_vhost' in self.config:
            self.rmq_vhost = self.config['rmq_vhost']

        if 'rmq_exchange_type' in self.config:
            self.rmq_exchange_type = self.config['rmq_exchange_type']

        if 'rmq_durable' in self.config:
            self.rmq_durable = bool(self.config['rmq_durable'])

        if 'rmq_heartbeat_interval' in self.config:
            self.rmq_heartbeat_interval = int(
                self.config['rmq_heartbeat_interval'])

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

    def _bind_all(self):
        """
        Bind all RMQ servers defined in config
        """
        for rmq_server in self.rmq_server:
            self._bind(rmq_server)

    def _bind(self, rmq_server):
        """
           Create PUB socket and bind
        """
        if (rmq_server in self.connections.keys()
                and self.connections[rmq_server] is not None
                and self.connections[rmq_server].is_open):
            # It seems we already have this server, so let's try _unbind just
            # to be safe.
            self._unbind(rmq_server)

        credentials = None
        if self.rmq_user and self.rmq_password:
            credentials = pika.PlainCredentials(
                self.rmq_user,
                self.rmq_password)

        parameters = pika.ConnectionParameters(
            host=rmq_server,
            port=self.rmq_port,
            virtual_host=self.rmq_vhost,
            credentials=credentials,
            heartbeat_interval=self.rmq_heartbeat_interval,
            retry_delay=5,
            connection_attempts=3)

        self.connections[rmq_server] = None
        while (self.connections[rmq_server] is None
                or self.connections[rmq_server].is_open is False):
            try:
                self.connections[rmq_server] = pika.BlockingConnection(
                    parameters)
                self.channels[rmq_server] = self.connections[
                    rmq_server].channel()
                self.channels[rmq_server].exchange_declare(
                    exchange=self.rmq_exchange,
                    type=self.rmq_exchange_type,
                    durable=self.rmq_durable)
                # Reset reconnect_interval after a successful connection
                self.reconnect_interval = 1
            except Exception, exception:
                self.log.debug("Caught exception in _bind: %s", exception)
                if rmq_server in self.connections.keys():
                    self._unbind(rmq_server)

                if self.reconnect_interval >= 16:
                    break

                if self.reconnect_interval < 16:
                    self.reconnect_interval = self.reconnect_interval * 2

                time.sleep(self.reconnect_interval)

    def _unbind(self, rmq_server=None):
        """ Close AMQP connection and unset channel """
        try:
            self.connections[rmq_server].close()
        except AttributeError:
            pass

        self.connections[rmq_server] = None
        self.channels[rmq_server] = None

    def __del__(self):
        """
          Destroy instance of the rmqHandler class
        """
        if hasattr(self, 'connections'):
            for rmq_server in self.connections.keys():
                self._unbind(rmq_server)

    def process(self, metric):
        """
          Process a metric and send it to RMQ pub socket
        """
        for rmq_server in self.connections.keys():
            try:
                if (self.connections[rmq_server] is None
                        or self.connections[rmq_server].is_open is False):
                    self._bind(rmq_server)

                channel = self.channels[rmq_server]
                channel.basic_publish(exchange=self.rmq_exchange,
                                      routing_key='', body="%s" % metric)
            except Exception, exception:
                self.log.error(
                    "Failed publishing to %s, attempting reconnect",
                    rmq_server)
                self.log.debug("Caught exception: %s", exception)
                self._unbind(rmq_server)
                self._bind(rmq_server)
