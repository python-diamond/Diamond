
import subprocess

import diamond.collector

class PingCollector(diamond.collector.Collector):
    """
    Collect icmp round trip times
    Only valid for ipv4 hosts currently
    """

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        return {
            'path':     'ping',
        }

    def collect(self):
        for key in self.config.keys():
            if key[:7] == "target_":
                host = self.config[key]
                metric_name = "ping."+host.replace('.','_');

                ping = subprocess.Popen(["ping", '-nq', '-c 1', host], stdout=subprocess.PIPE).communicate()[0].strip().split("\n")[-1]
                if ping[0:3] != 'rtt':
                    metric_value = 10000
                else :
                    ping = ping.split()[3].split('/')[0]
                    metric_value = int(round(float(ping)))
                self.publish(metric_name, metric_value)
