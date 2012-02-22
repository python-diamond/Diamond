
from diamond import *
import diamond.collector
import diamond.convertor

_KEY_MAPPING = [
    'MemTotal'     ,
    'MemFree'      ,
    'Buffers'      ,
    'Cached'       ,
    'Active'       ,
    'Dirty'        ,
    'Inactive'     ,
    'SwapTotal'    ,
    'SwapFree'     ,
    'SwapCached'   ,
    'VmallocTotal' ,
    'VmallocUsed'  ,
    'VmallocChunk'
]

class MemoryCollector(diamond.collector.Collector):
    """
    This class collects data on memory utilization

    /proc/meminfo is used to gather the data, which is returned in units of kB
    """

    PROC = '/proc/meminfo'

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        return {
            'enabled':  'True',
            'path':     'memory',
            'method':   'Threaded',
            # Collect all the nodes or just a few standard ones?
            # Uncomment to enable
            #'detailed' : 'True'
        }

    def collect(self):
        """
        Collect memory stats
        """
        if not os.access(self.PROC, os.R_OK):
            return None

        file = open(self.PROC)
        data = file.read()
        file.close()

        for line in data.splitlines():
            try:
                name, value, units = line.split()
                name = name.rstrip(':')
                value = int(value)

                if name not in _KEY_MAPPING and not self.config.has_key('detailed'):
                    continue

                value = diamond.convertor.binary.convert(value = value, oldUnit = units, newUnit = self.config['byte_unit'])

                self.publish(name, value)
            except ValueError:
                continue
