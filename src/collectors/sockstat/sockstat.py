
from diamond import *
import diamond.collector

_RE = re.compile('|'.join([
    r'sockets: used (?P<used>\d+)',
    r'TCP: inuse (?P<tcp_inuse>\d+) orphan (?P<tcp_orphan>\d+) tw (?P<tcp_tw>\d+) alloc (?P<tcp_alloc>\d+) mem (?P<tcp_mem>\d+)',
    r'UDP: inuse (?P<udp_inuse>\d+) mem (?P<udp_mem>\d+)'
]))

class SockstatCollector(diamond.collector.Collector):
    """
    Uses /proc/net/sockstat to collect data on number of open sockets
    """

    PROC = '/proc/net/sockstat'

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        return {
            'enabled':  'True',
            'path':     'sockets',
            'method':   'Threaded',
        }

    def collect(self):
        if not os.access(self.PROC, os.R_OK):
            return None

        result = {}

        file = open(self.PROC)
        for line in file:
            match = _RE.match(line)
            if match:
                for key, value in match.groupdict().items():
                    if value:
                        result[key] = int(value)
        file.close()

        for key, value in result.items():
            self.publish(key, value)
