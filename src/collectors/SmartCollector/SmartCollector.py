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
            'devices': '^disk[0-9]$|^sd[a-z]$|^hd[a-z]$',
            'method': 'Threaded'
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
                    attribute = attr.split()
                    if attribute[1] != "Unknown_Attribute":
                        self.publish("%s.%s" % (device, attribute[1]), attribute[9])
                    else:
                        self.publish("%s.%s" % (device, attribute[0]), attribute[9])
