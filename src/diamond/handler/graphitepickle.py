import struct

from GraphiteHandler import GraphiteHandler

try:
	import cPickle as pickle
except:
	import pickle as pickle

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
