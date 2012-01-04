
from diamond import *
import diamond.collector

class CPUCollector(diamond.collector.Collector):
    """
    The CPUCollector collects CPU utilization metric using /proc/stat.
    """

    PROC = '/proc/stat'
    MAX_VALUES = {
        'user': diamond.collector.MAX_COUNTER,
        'nice': diamond.collector.MAX_COUNTER,
        'system': diamond.collector.MAX_COUNTER,
        'idle': diamond.collector.MAX_COUNTER,
        'iowait': diamond.collector.MAX_COUNTER,
    }

    def collect(self):
        """
        Collector cpu stats
        """
        if not os.access(self.PROC, os.R_OK):
            return None

        results = {}
        # Open file
        file = open(self.PROC)
        # Build Regex
        exp = '^(cpu[0-9]*)\s+(?P<user>\d+)\s+(?P<nice>\d+)\s+(?P<system>\d+)\s+(?P<idle>\d+)\s+(?P<iowait>\d+).*$'
        reg = re.compile(exp)
        for line in file:
            match = reg.match(line)

            if match:
                cpu = match.group(1)
                if cpu == 'cpu':
                    cpu = 'total'
                results[cpu] = {}
                results[cpu] = match.groupdict()
        # Close File
        file.close()

        for cpu in results.keys():
            stats = results[cpu]
            for s in stats.keys():
                # Get Metric Name
                metric_name = '.'.join([cpu, s])
                # Publish Metric Derivative
                self.publish(metric_name, self.derivative(metric_name, long(stats[s]), self.MAX_VALUES[s]))
