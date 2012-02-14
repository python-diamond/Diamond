from handler import Handler
import logging
import logging.handlers

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
