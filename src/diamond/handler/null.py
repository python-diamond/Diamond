# coding=utf-8

"""
Output the collected values to the debug log channel.
"""

from Handler import Handler


class NullHandler(Handler):
    """
    Implements the abstract Handler class, doing nothing except log
    """
    def process(self, metric):
        """
        Process a metric by doing nothing
        """
        self.log.debug("Process: %s", str(metric).rstrip())
