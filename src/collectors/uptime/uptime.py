from diamond.collector import Collector
from diamond import convertor

import os

procpath = '/proc/uptime'
metric_name = 'minutes'


class UptimeCollector(Collector):
    def get_default_config(self):
        config = super(UptimeCollector, self).get_default_config()
        config.update({
            'path': 'uptime',
        })
        return config

    def collect(self):
        if not os.path.exists(procpath):
            self.log.error('Input path %s does not exist' % procpath)
            return {}

        v = self.read()
        if not v is None:
            self.publish(metric_name, v)

    def read(self):
        try:
            fd = open(procpath)
            uptime = fd.readline()
            fd.close()
            v = float(uptime.split()[0].strip())
            return convertor.time.convert(v, 's', 'm')
        except Exception, e:
            self.log.error('Unable to read uptime from %s: %s' % (procpath, e))
            return None
