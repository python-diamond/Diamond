
from diamond import *
import diamond.collector

class VMStatCollector(diamond.collector.Collector):
    """
    Uses /proc/vmstat to collect data on virtual memory manager
    """

    PROC = '/proc/vmstat'
    MAX_VALUES = {
        'pgpgin' : diamond.collector.MAX_COUNTER,
        'pgpgout': diamond.collector.MAX_COUNTER,
        'pswpin' : diamond.collector.MAX_COUNTER,
        'pswpout': diamond.collector.MAX_COUNTER,
    }

    def collect(self):
        if not os.access(self.PROC, os.R_OK):
            return None

        results = {}
        # open file
        file = open(self.PROC)
        exp = '^(pgpgin|pgpgout|pswpin|pswpout)\s(\d+)'
        reg = re.compile(exp)
        # Build regex
        for line in file:
            match = reg.match(line)
            if match:
                name = match.group(1)
                value = match.group(2)
                results[name] = self.derivative(name, int(value), self.MAX_VALUES[name])

        # Close file
        file.close()

        for key, value in results.items():
            self.publish(key, value, 2)
