"""
Shells out to get the exim queue length

#### Dependencies

 * /usr/sbin/exim

"""

import diamond.collector
import subprocess
import os

class EximCollector(diamond.collector.Collector):
  
    COMMAND = ['/usr/sbin/exim', '-bpc']
    
    def get_default_config_help(self):
        config_help = super(EximCollector, self).get_default_config_help()
        config_help.update({
        })
        return config_help
    
    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(EximCollector, self).get_default_config()
        config.update(  {
            'path' : 'exim',
            'method' : 'threaded'
        } )
        return config

    def collect(self):
        if not os.access(EximCollector.COMMAND[0], os.X_OK):
            return
        queuesize = subprocess.Popen(EximCollector.COMMAND, stdout=subprocess.PIPE).communicate()[0].split()
        if not len(queuesize):
            return
        queuesize = queuesize[-1]
        self.publish('queuesize', queuesize)
