import diamond.collector
import subprocess
import re
import os

class SmartCollector(diamond.collector.Collector):
    """
    Collect data from S.M.A.R.T.'s attribute reporting.
    """

    def get_default_config(self):
        """
        Returns default configuration options.
        """
        return {
            'path': 'smart',
            'devices': '^disk[0-9]$|^sd[a-z]$|^hd[a-z]$'
        }

    def collect(self):
        """
        Collect and publish S.M.A.R.T. attributes
        """
        devices = re.compile(self.config['devices'])

        for device in os.listdir('/dev'):
            if devices.match(device):
                attributes = subprocess.Popen(["smartctl", "-A", os.path.join('/dev',device)],
                             stdout=subprocess.PIPE).communicate()[0].strip().splitlines()

                for attr in attributes[7:]:
                    self.publish("%s.%s" % (device, attr.split()[1]), attr.split()[9])
