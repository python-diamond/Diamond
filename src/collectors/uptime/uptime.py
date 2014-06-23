from diamond.collector import Collector
from diamond import convertor

import os

procpath = '/proc/uptime'
metric_name = 'minutes'


def read():
    try:
        fd = open(procpath)
        uptime = fd.readline()
    finally:
        fd.close()
    v = float(uptime.split()[0].strip())
    return convertor.time.convert(v, 's', 'm')


class UptimeCollector(Collector):
    def get_default_config(self):
        config = super(UptimeCollector, self).get_default_config()
        config.update({
            'path': 'uptime',
        })
        return config

    def collect(self):
        if not os.path.exists(procpath):
            self.log.error('path: {0} not found'.format(procpath))
            return {}

        try:
            v = read()
        except Exception as e:
            self.log.exception(e)

        self.publish(metric_name, v)
