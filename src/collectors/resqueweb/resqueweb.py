
import urllib2

import diamond.collector


class ResqueWebCollector(diamond.collector.Collector):
    def get_default_config(self):
        """
        Returns the default collector settings
        """
        return { 
            'host': 'localhost',
            'port': 5678,
            'path': 'resqueweb', 
        }

    def get_resque_output(self):
        try:
            response = urllib2.urlopen('http://%s:%d/stats.txt' % (self.config['host'], int(self.config['port'])))
        except Exception, e:
            self.log.error('Couldnt connect to resque-web: %s', e)
            return {}

    def collect(self):
        output = self.get_resque_output()
        
        for data in output.split("\n"):
            if data == "":
                continue
                
            item,count = data.strip().split("=")

            try:
                count = int(count)
                (item, queue) = item.split(".")

                if item == "resque":
                    if queue[-1] == "+":
                        self.publish("%s.total" % queue.replace("+", ""), count)
                    else:
                        self.publish("%s.current" % queue, count)
                else:
                    self.publish("queue.%s.current" % queue, count)

                
            except Exception, e:
                self.log.error('Couldnt parse the queue: %s', e)

