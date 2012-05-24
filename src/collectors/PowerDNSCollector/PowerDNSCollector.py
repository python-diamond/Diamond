import diamond.collector
import subprocess

class PowerDNSCollector(diamond.collector.Collector):
    """
    Collects all metrics exported by the powerdns nameserver using the
    pdns_control binary.
    """ 
    _GAUGE_KEYS = [
        'cache-bytes', 'cache-entries', 'chain-resends',
        'concurrent-queries', 'dlg-only-drops', 'dont-outqueries',
        'ipv6-outqueries', 'latency', 'max-mthread-stack', 'negcache-entries',
        'nsspeeds-entries',
        'packetcache-bytes', 'packetcache-entries', 'packetcache-size',
        'qa-latency', 'throttle-entries'
        ]
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
            try:
                value = float(value)
            except:
                pass
            if metric not in self._GAUGE_KEYS:
                value = self.derivative(metric, value)
                if value < 0:
                    continue
            self.log.info("Metric %s has value %d", metric, int(value))
            self.publish(metric, value)
