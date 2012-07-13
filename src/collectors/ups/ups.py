"""
This class collects data from NUT, a UPS interface for linux.

#### Dependencies

 * nut/upsc to be installed, configured and running.

"""

import diamond.collector
import os
import subprocess

class UPSCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(UPSCollector, self).get_default_config_help()
        config_help.update({
            'ups_name' : 'The name of the ups to collect data for',
            'bin' : 'The path to the upsc binary',
        })
        return config_help

    def get_default_config(self):
        """
        Returns default collector settings.
        """

        config = super(UPSCollector, self).get_default_config()
        config.update(  {
            'path': 'ups',
            'ups_name': 'cyberpower',
            'bin': '/bin/upsc'
        } )
        return config

    def collect(self):
        if not os.access(self.config['bin'], os.X_OK):
            self.log.error(self.config['bin']+" is not executable")
            return False
        
        p = subprocess.Popen([self.config['bin'], self.config['ups_name']], stdout=subprocess.PIPE)

        for ln in p.communicate()[0].splitlines():
            datapoint = ln.split(": ")

            try:
                val = float(datapoint[1])
            except:
                continue

            if len(datapoint[0].split(".")) == 2:
                # If the metric name is the same as the subfolder
                # double it so it's visible.
                name = ".".join([datapoint[0], datapoint[0].split(".")[1]])
            else:
                name = datapoint[0]

            self.publish(name, val)
