import diamond.collector
import subprocess
import os

class PowerDNSCollector(diamond.collector.Collector):
    """
    Collects all metrics exported by the powerdns nameserver using the
    pdns_control binary.
    
    #### Dependencies

    * pdns_control
    
    """
    
    _GAUGE_KEYS = [
        'cache-bytes', 'cache-entries', 'chain-resends',
        'concurrent-queries', 'dlg-only-drops', 'dont-outqueries',
        'ipv6-outqueries', 'latency', 'max-mthread-stack', 'negcache-entries',
        'nsspeeds-entries',
        'packetcache-bytes', 'packetcache-entries', 'packetcache-size',
        'qa-latency', 'throttle-entries'
        ]
    
    def get_default_config_help(self):
        config_help = super(PowerDNSCollector, self).get_default_config_help()
        config_help.update({
            'pdns_control' : 'Path to pdns_control binary',
        })
        return config_help
    
    def get_default_config(self): 
        """
        Returns the default collector settings
        """
        config = super(PowerDNSCollector, self).get_default_config()
        config.update(  { 
            'pdns_control': '/usr/bin/pdns_control', 
            'path': 'powerdns', 
        } )
        return config

    def collect(self):
        if not os.access(self.config['pdns_control'], os.X_OK):
            self.log.error(self.config['pdns_control']+" is not executable")
            return False
        
        sp = subprocess.Popen([self.config['pdns_control'], "list"], stdout=subprocess.PIPE)
        data = sp.communicate()[0]
        for metric in data.split(','):
            if not metric.strip():
                continue
            metric, value = metric.split('=')
            try:
                value = float(value)
            except:
                pass
            if metric not in self._GAUGE_KEYS:
                value = self.derivative(metric, value)
                if value < 0:
                    continue
            self.publish(metric, value)
