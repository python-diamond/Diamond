from handler import Handler
import socket

class GraphiteHandler(Handler):
    """
    Implements the abstract Handler class, sending data to graphite
    """
    RETRY = 3

    def __init__(self, config=None):
        """
        Create a new instance of the GraphiteHandler class
        """
        # Initialize Handler
        Handler.__init__(self, config)

        # Initialize Data
        self.socket = None

        # Initialize Options
        self.host = self.config['host']
        self.port = int(self.config['port'])
        self.timeout = int(self.config['timeout'])

        # Connect
        self._connect()

    def __del__(self):
        """
        Destroy instance of the GraphiteHandler class
        """
        self._close()

    def process(self, metric):
        """
        Process a metric by sending it to graphite
        """
        # Acquire lock
        self.lock.acquire()
        # Just send the data as a string
        self._send(str(metric))
        # Release lock
        self.lock.release()

    def _send(self, data):
        """
        Send data to graphite. Data that can not be sent will be queued.
        """
        retry = self.RETRY
        # Attempt to send any data in the queue
        while retry > 0:
            # Check socket
            if not self.socket:
                # Log Error
                self.log.error("GraphiteHandler: Socket unavailable.")
                # Attempt to restablish connection
                self._connect()
                # Decrement retry
                retry -= 1
                # Try again
                continue
            try:
                # Send data to socket
                self.socket.sendall(data)
                # Done
                break
            except socket.error, e:
                # Log Error
                self.log.error("GraphiteHandler: Failed sending data. %s." % (e))
                # Attempt to restablish connection
                self._close()
                # Decrement retry
                retry -= 1
                # try again
                continue

    def _connect(self):
        """
        Connect to the graphite server
        """
        # Create socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if socket is None:
            # Log Error
            self.log.error("GraphiteHandler: Unable to create socket.")
            # Close Socket
            self._close()
            return
        # Set socket timeout
        self.socket.settimeout(self.timeout)
        # Connect to graphite server
        try:
            self.socket.connect((self.host, self.port))
            # Log
            self.log.debug("Established connection to graphite server %s:%d" % (self.host, self.port))
        except Exception, ex:
            # Log Error
            self.log.error("GraphiteHandler: Failed to connect to %s:%i. %s" % (self.host, self.port, ex))
            # Close Socket
            self._close()
            return

    def _close(self):
        """
        Close the socket
        """
        if self.socket is not None:
            self.socket.close()
        self.socket = None
