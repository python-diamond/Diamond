
from diamond import *
import diamond.collector

_RE = re.compile(r'(\d+)\s+(\d+)\s+(\d+)')

class FilestatCollector(diamond.collector.Collector):
    """
    Uses /proc/sys/fs/file-nr to collect data on number of open files
    """

    PROC = '/proc/sys/fs/file-nr'

    def collect(self):
        if not os.access(self.PROC, os.R_OK):
            return None

        file = open(self.PROC)
        for line in file:
            match = _RE.match(line)
            if match:
                self.publish('assigned', int(match.group(1)))
                self.publish('unused',   int(match.group(2)))
                self.publish('max',      int(match.group(3)))
        file.close()
