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
        self.log.debug("Metric: %s", str(metric).rstrip().replace(' ', '\t'))

    def get_default_config_help(self):
        """
        Returns the help text for the configuration options for this handler
        """
        config = super(NullHandler, self).get_default_config_help()

        config.update({
        })

        return config

    def get_default_config(self):
        """
        Return the default config for the handler
        """
        config = super(NullHandler, self).get_default_config()

        config.update({
        })

        return config
