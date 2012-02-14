
from diamond import *
import diamond.collector
import diamond.convertor

import commands

class UserScriptsCollector(diamond.collector.Collector):
    """
    Runs third party scripts and collects their output
    """
    def collect(self):
        scripts_path = self.config['scripts_path']
        if not os.access(scripts_path, os.R_OK):
            return None
        for script in os.listdir(scripts_path):
            if not os.access(os.path.join(scripts_path, script), os.X_OK):
                continue
            stat, out = commands.getstatusoutput(os.path.join(scripts_path, script))
            if stat != 0:
                continue
            for line in out.split('\n'):
                name, value = line.split()
                self.publish(name, value)

