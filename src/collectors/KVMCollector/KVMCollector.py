
from diamond import *
import diamond.collector
import os

class KVMCollector(diamond.collector.Collector):
    """
    Collects /sys/kernel/debug/kvm/*
    """
    
    PROC = '/sys/kernel/debug/kvm'
    
    
    def get_default_config(self):
        """
        Returns the default collector settings
        """
        return {
            'path' : 'kvm',
        }

    def collect(self):
        if not os.path.isdir(self.PROC):
            self.log.error('/sys/kernel/debug/kvm is missing. Did you "mount -t debugfs debugfs /sys/kernel/debug"?')
            return {}
            
        for file in os.listdir(self.PROC):
            filepath = os.path.abspath(os.path.join(self.PROC, file))
            fh = open(filepath, 'r')
            metric_value = self.derivative(file, float(fh.readline()), 4294967295)
            self.publish(file, metric_value)
