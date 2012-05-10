from Handler import Handler
import statsd
import logging


class StatsdHandler(Handler):
    """
    Implements the abstract Handler class, sending data to statsd.
    This is a UDP service, sending datagrams.  They may be lost.
    It's OK.
    """
    def __init__(self, config=None):
        """
        Create a new instance of the StatsdHandler class
        """
        # Initialize Handler
        Handler.__init__(self, config)
        logging.debug("Initialized statsd handler.")
        # Initialize Options
        self.host = self.config['host']
        self.port = int(self.config['port'])

        # Connect
        self._connect()

    def process(self, metric):
        """
        Process a metric by sending it to statsd
        """
        # Acquire lock
        self.lock.acquire()
        # Just send the data as a string
        self._send(metric)
        # Release lock
        self.lock.release()

    def _send(self, metric):
        """
        Send data to statsd. Fire and forget.  Cross fingers and it'll arrive.
        """
        # Split the path into a prefix and a name
        # to work with the statsd module's view of the world.
        # It will get re-joined by the python-statsd module.
        (prefix, name) = metric.path.rsplit(".", 1)
        logging.debug("Sending {0} {1} {2}|r".format(name, metric.value, metric.timestamp))
        statsd.Raw(prefix, self.connection).send(name, metric.value, metric.timestamp)

    def _connect(self):
        """
        Connect to the statsd server
        """
        # Create socket
        self.connection = statsd.Connection(
            host=self.host,
            port=self.port,
            sample_rate=1.0
        )
