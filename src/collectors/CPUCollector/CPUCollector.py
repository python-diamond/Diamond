
from diamond import *
import diamond.collector

try:
    import psutil
except ImportError:
    psutil = None

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
    
    def get_default_config(self):
        """
        Returns the default collector settings
        """
        return {
            'enabled':  'True',
            'path':     'cpu'
        }

    def collect(self):
        """
        Collector cpu stats
        """
        if os.access(self.PROC, os.R_OK):
    
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
            return True
        
        elif psutil:
            cpu_time = psutil.cpu_times(True)
            total_time = psutil.cpu_times()
            for i in range(0, len(cpu_time)):
                metric_name = 'cpu'+str(i)
                self.publish(metric_name+'.user',   self.derivative(metric_name+'.user',   cpu_time[i].user,   self.MAX_VALUES['user']))
                self.publish(metric_name+'.nice',   self.derivative(metric_name+'.nice',   cpu_time[i].nice,   self.MAX_VALUES['nice']))
                self.publish(metric_name+'.system', self.derivative(metric_name+'.system', cpu_time[i].system, self.MAX_VALUES['system']))
                self.publish(metric_name+'.idle',   self.derivative(metric_name+'.idle',   cpu_time[i].idle,   self.MAX_VALUES['idle']))
            
            metric_name = 'total'
            self.publish(metric_name+'.user',   self.derivative(metric_name+'.user',   total_time.user,   self.MAX_VALUES['user']))
            self.publish(metric_name+'.nice',   self.derivative(metric_name+'.nice',   total_time.nice,   self.MAX_VALUES['nice']))
            self.publish(metric_name+'.system', self.derivative(metric_name+'.system', total_time.system, self.MAX_VALUES['system']))
            self.publish(metric_name+'.idle',   self.derivative(metric_name+'.idle',   total_time.idle,   self.MAX_VALUES['idle']))
        
            return True
        
        return None
