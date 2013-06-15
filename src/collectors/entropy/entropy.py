# coding=utf-8

"""
Uses /proc to collect available entropty

#### Dependencies

 * /proc/sys/kernel/random/entropy_avail

"""

import diamond.collector
import os


class EntropyStatCollector(diamond.collector.Collector):

    PROC = '/proc/sys/kernel/random/entropy_avail'

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(EntropyStatCollector, self).get_default_config()
        config.update({
            'enabled':  'True',
            'path':     'entropy'
        })
        return config

    def collect(self):
        if not os.access(self.PROC, os.R_OK):
            return None

        # open file
        file = open(self.PROC)
	# read value
	entropy = file.read().strip()

        # Close file
        file.close()

	# Publish value
	self.publish_gauge("available", entropy)
