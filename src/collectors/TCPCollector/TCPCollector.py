
from diamond import *
import diamond.collector

class TCPCollector(diamond.collector.Collector):
    """
    The TCPCollector class collects metrics on TCP stats from
    /proc/net/netstat
    """

    PROC='/proc/net/netstat'

    def collect(self):
        if not os.access(self.PROC, os.R_OK):
            return None

        lines = []

        file = open(self.PROC)
        for line in file:
            if line.startswith("TcpExt:"):
                lines.append(line[7:].split())
        file.close()

        if len(lines) == 0:
            return

        if len(lines) != 2:
            return

        # There are two lines in lines: names and values, space-separated.
        names, values = lines
        allowed_names = self.config['allowed_names']

        for key, value in zip(names, values):
            if key in allowed_names:
                self.publish(key, value, 0)
