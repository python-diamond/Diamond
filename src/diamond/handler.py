# Copyright (C) 2010-2011 by Brightcove Inc. 
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import socket
import logging
import logging.handlers
import threading
import cPickle as pickle
import struct
from collections import deque

from metric import Metric 

class Handler(object):
    """
    Handlers process metrics that are collected by Collectors.
    """
    def __init__(self, config=None):
        """
        Create a new instance of the Handler class
        """
        # Initialize Log
        self.log = logging.getLogger('diamond')
        # Initialize Data
        self.config = config
        # Initialize Lock
        self.lock = threading.Condition(threading.Lock())

    def process(self, metric):
        """
        Process a metric 

        Should be overridden in subclasses
        """
        raise NotImplementedException 

class ArchiveHandler(Handler):
    """
    Implements the Handler abstract class, archiving data to a log file 
    """
    def __init__(self, config):
        """
        Create a new instance of the ArchiveHandler class
        """
        # Initialize Handler
        Handler.__init__(self, config)

        # Create Archive Logger
        self.archive = logging.getLogger('archive')
        self.archive.setLevel(logging.DEBUG)
        # Create Archive Log Formatter        
        formatter = logging.Formatter('%(message)s')
        # Create Archive Log Handler
        handler = logging.handlers.TimedRotatingFileHandler(self.config['log_file'], 'midnight', 1, backupCount=int(self.config['days']))
        handler.setFormatter(formatter)
        handler.setLevel(logging.DEBUG)
        self.archive.addHandler(handler)

    def process(self, metric):
        """
        Send a Metric to the Archive. 
        """
        # Acquire Lock    
        self.lock.acquire()
        # Archive Metric
        self.archive.info(str(metric).strip())
        # Release Lock
        self.lock.release()

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

class GraphitePickleHandler(GraphiteHandler):
    """
    Overrides the GraphiteHandler class, sending data to graphite using batched pickle format
    """
    def __init__(self, config=None):
        """
        Create a new instance of the GraphitePickleHandler 
        """
        # Initialize GraphiteHandler
        GraphiteHandler.__init__(self, config)
        # Initialize Data
        self.batch = []
        # Initialize Options
        self.batch_size = int(self.config['batch'])

    def process(self, metric):
        # Acquire lock    
        self.lock.acquire()
        # Convert metric to pickle format
        m = (metric.path, (metric.timestamp, metric.value) )
        # Add the metric to the match
        self.batch.append(m)
        # If there are sufficient metrics, then pickle and send
        if len(self.batch) >= self.batch_size:
            # Log
            self.log.debug("GraphitePickleHandler: Sending batch data. batch size: %d" % (self.batch_size))
            # Pickle the batch of metrics
            data = self._pickle_batch()
            # Send pickled batch
            self._send(data)
            # Clear Batch
            self.batch = []
        # Release lock 
        self.lock.release()

    def _pickle_batch(self):
        """
        Pickle the metrics into a form that can be understood by the graphite pickle connector.
        """
        # Pickle 
        payload = pickle.dumps(self.batch)
        
        # Pack Message
        header = struct.pack("!L", len(payload))
        message = header + payload

        # Return Message
        return message

class NullHandler(Handler):
    """
    Implements the abstract Handler class, doing nothing except log 
    """
    def process(self, metric):
        """
        Process a metric by doing nothing 
        """
        self.log.debug("Process: %s" % (str(metric).rstrip())) 

