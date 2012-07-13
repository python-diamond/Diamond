"""
Collect icmp round trip times
Only valid for ipv4 hosts currently

#### Dependencies

 * ping
 
#### Configuration

Configuration is done by adding in extra keys like this

 * target_1 - example.org
 * target_fw - 192.168.0.1
 * target_localhost - localhost

We extract out the key after target_ and use it in the graphite node we push.

"""

import subprocess
import diamond.collector

class PingCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(PingCollector, self).get_default_config_help()
        config_help.update({
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(PingCollector, self).get_default_config()
        config.update(  {
            'path':     'ping',
        } )
        return config

    def collect(self):
        for key in self.config.keys():
            if key[:7] == "target_":
                host = self.config[key]
                metric_name = host.replace('.','_');

                ping = subprocess.Popen(["ping", '-nq', '-c 1', host], stdout=subprocess.PIPE).communicate()[0].strip().split("\n")[-1]
                
                # Linux
                if ping.startswith('rtt'):
                    ping = ping.split()[3].split('/')[0]
                    metric_value = int(round(float(ping)))
                # OS X
                elif ping.startswith('round-trip '):
                    ping = ping.split()[3].split('/')[0]
                    metric_value = int(round(float(ping)))
                # Unknown
                else :
                    metric_value = 10000
                    
                self.publish(metric_name, metric_value)
