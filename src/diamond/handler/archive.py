# coding=utf-8

"""
Write the collected stats to a locally stored log file. Rotate the log file
every night and remove after 7 days.
"""

from Handler import Handler
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
        handler = logging.handlers.TimedRotatingFileHandler(
            filename=self.config['log_file'],
            when='midnight',
            interval=1,
            backupCount=int(self.config['days']),
            encoding=self.config['encoding']
            )
        handler.setFormatter(formatter)
        handler.setLevel(logging.DEBUG)
        self.archive.addHandler(handler)

    def get_default_config_help(self):
        """
        Returns the help text for the configuration options for this handler
        """
        config = super(ArchiveHandler, self).get_default_config_help()

        config.update({
            'log_file': 'Path to the logfile',
            'days': 'How many days to store',
            'encoding': '',
        })

        return config

    def get_default_config(self):
        """
        Return the default config for the handler
        """
        config = super(ArchiveHandler, self).get_default_config()

        config.update({
            'log_file': '',
            'days': 7,
            'encoding': None,
        })

        return config

    def process(self, metric):
        """
        Send a Metric to the Archive.
        """
        # Archive Metric
        self.archive.info(str(metric).strip())
