# coding=utf-8

"""
Collects data for Resque Web

#### Dependencies

 * urllib2

"""

import urllib2
import diamond.collector


class ResqueWebCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(ResqueWebCollector, self).get_default_config_help()
        config_help.update({
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(ResqueWebCollector, self).get_default_config()
        config.update({
            'host': 'localhost',
            'port': 5678,
            'path': 'resqueweb',
        })
        return config

    def collect(self):
        try:
            response = urllib2.urlopen("http://%s:%s/stats.txt" % (
                self.config['host'], int(self.config['port'])))
        except Exception, e:
            self.log.error('Couldnt connect to resque-web: %s', e)
            return {}

        for data in response.read().split("\n"):
            if data == "":
                continue

            item, count = data.strip().split("=")
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
