
import subprocess

import diamond.collector

class PostqueueCollector(diamond.collector.Collector):
    """
    Collect the emails in the postfix queue
    """

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        return {
            'path':     'postqueue',
        }

    def get_postqueue_output(self):
        try:
            return subprocess.Popen(["postqueue", "-p"], stdout=subprocess.PIPE).communicate()[0]
        except:
            return ""

    def collect(self):
        output = self.get_postqueue_output()
        
        try:
            postqueue_count = int(output.strip().split("\n")[-1].split()[-2])
        except:
            postqueue_count = 0

        self.publish('count', postqueue_count)

