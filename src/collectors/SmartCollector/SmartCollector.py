
import subprocess
import os
import re
import diamond.collector

class SmartCollector(diamond.collector.Collector):
    '''
    Collect smart attributes
    '''
    
    def get_default_config(self):
        """
        Returns the default collector settings
        """
        return {
            'enabled':  'False',
            'path':     'smart',
            'devices':  "^disk[0-9]$|^sd[a-z]$|^hd[a-z]$",
        }    
    
    def getDisks(self):
        '''
        Return a list of devices that match the config file regex
        '''
        disks = []
        for device in os.listdir('/dev/'):
            if re.match(self.config['devices'], device):
                disks.append(device);
        return disks
    
    def getSmartAttributes(self, disk):
        '''
        Return a list of smart attributes in truple form
        '''
        list = []
        attributes = subprocess.Popen(["smartctl", "-A", "/dev/"+disk], stdout=subprocess.PIPE).communicate()[0].strip().split("\n")
        for attribute in attributes[7:]:
            attribute = attribute.split()
            list.append((disk+'.'+attribute[0]+'-'+attribute[1], attribute[9]))
        return list

    def collect(self):
        for device in self.getDisks():
            attributes = self.getSmartAttributes(device)
            for attribute in attributes:
                metric_name = attribute[0]
                metric_value = round(self.derivative(metric_name, float(attribute[1])), 2)
                self.publish(metric_name, metric_value)
