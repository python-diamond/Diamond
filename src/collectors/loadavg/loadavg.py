import diamond.collector
import re
import os

_RE = re.compile(r'([\d.]+) ([\d.]+) ([\d.]+) (\d+)/(\d+)')

class LoadAverageCollector(diamond.collector.Collector):
    """
    Uses /proc/loadavg to collect data on load average
    """

    PROC = '/proc/loadavg'

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        return {
            'enabled':  'True',
            'path':     'loadavg',
            'method':   'Threaded'
        }

    def collect(self):
        if not os.access(self.PROC, os.R_OK):
            return None

        file = open(self.PROC)
        for line in file:
            match = _RE.match(line)
            if match:
                self.publish('01', float(match.group(1)), 2)
                self.publish('05', float(match.group(2)), 2)
                self.publish('15', float(match.group(3)), 2)
                self.publish('processes_running', int(match.group(4)))
                self.publish('processes_total',   int(match.group(5)))
        file.close()
