"""
Shells out to get the value of sysctl net.netfilter.nf_conntrack_count

#### Dependencies

 * /sbin/sysctl

"""

import diamond.collector
import subprocess
import os
import re

_RE = re.compile(r'^([a-z\._]*) = ([0-9]*)$')

class ConnTrackCollector(diamond.collector.Collector):

    COMMAND = ['/sbin/sysctl', 'net.netfilter.nf_conntrack_count']

    def get_default_config_help(self):
        config_help = super(ConnTrackCollector, self).get_default_config_help()
        config_help.update({
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(ConnTrackCollector, self).get_default_config()
        config.update( {
            'path':     'conntrack'
        } )
        return config

    def collect(self):
        if not os.access(ConnTrackCollector.COMMAND[0], os.X_OK):
            self.log.error(ConnTrackCollector.COMMAND[0]+" is not executable")
            return False
        
        line = subprocess.Popen(ConnTrackCollector.COMMAND, stdout=subprocess.PIPE).communicate()[0]
        match = _RE.match(line)
        if match:
            self.publish('nf_conntrack_count', int(match.group(2)))
