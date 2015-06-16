# coding=utf-8

"""
The OozieCollector collects Oozie statistics (Jobs, Memory Usage, etc) using the instrumentation URI

#### Dependencies

 * requests

"""

import requests
from diamond.collector import Collector

class OozieCollector(Collector):

    def get_default_config_help(self):
        config_help = super(OozieCollector, self).get_default_config_help()
        config_help.update({
            'excluded_settings': 'settings strings to ignore',
            'port': 'port to connect to oozie on',
            'url_ext': 'The url path under <host>:<port>',
            'host': 'Host to connect to',
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(OozieCollector, self).get_default_config()
        config.update({
            'path':     '',
            'excluded_settings': ['logging', 'version'],
            'port': '11000',
            'url': '/oozie/v1/admin/instrumentation',
            'host': 'localhost',
        })
        return config

    def collect(self):
        oozie_url = "http://%s:%s%s" % \
                    (self.config['host'], self.config['port'],
                     self.config['url'])
        r = requests.get(oozie_url)
        results = r.json()
        for section, data in results.iteritems():
            for group in data:
                for key, val in group.iteritems():
                    grouping = group['group']
                    if 'data' in key:
                        for item in val:
                            metric_name = "%s.%s.%s" % (section, grouping,
                                                        item['name'].replace('.', '_'))
                            if any(x in metric_name for x in \
                                   self.config['excluded_settings']):
                                continue
                            try:
                                value = float(item['value'])
                            except Exception:
                                pass
                            else:
                                self.publish(metric_name, value)

