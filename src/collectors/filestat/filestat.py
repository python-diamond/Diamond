import diamond.collector
import re
import os

_RE = re.compile(r'(\d+)\s+(\d+)\s+(\d+)')

class FilestatCollector(diamond.collector.Collector):
    """
    Uses /proc/sys/fs/file-nr to collect data on number of open files
    """

    PROC = '/proc/sys/fs/file-nr'

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(FilestatCollector, self).get_default_config()
        config.update(  {
            'path':     'files',
            'method':   'Threaded'
        } )
        return config

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
