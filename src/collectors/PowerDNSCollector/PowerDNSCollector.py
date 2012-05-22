import diamond.collector
import subprocess

class PowerDNSCollector(diamond.collector.Collector):
    """
    Collects all metrics exported by the powerdns nameserver using the
    pdns_control binary.
    """ 
    def get_default_config(self): 
        """
        Returns the default collector settings
        """
        return { 
            'pdns_control': '/usr/bin/pdns_control', 
            'path': 'powerdns', 
        }

    def collect(self):
        sp = subprocess.Popen([self.config['pdns_control'], "list"], stdout=subprocess.PIPE)
        data = sp.communicate()[0]
        for metric in data.split(','):
            if not metric.strip():
                continue
            metric, value = metric.split('=')
            self.publish(metric, int(value))
