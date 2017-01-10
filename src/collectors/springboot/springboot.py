# coding=utf-8

"""
Collect the springboot metrics exposes by the actuator bean configured on
http://localhost:8080/metrics

#### Dependencies

 * urlib2

"""

import urllib2

try:
    import json
except ImportError:
    import simplejson as json

import diamond.collector


class SpringBootCollector(diamond.collector.Collector):
    def get_default_config_help(self):
        config_help = super(SpringBootCollector,
                            self).get_default_config_help()
        config_help.update({
            'host': "",
            'port': "",
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(SpringBootCollector, self).get_default_config()
        config.update({
            'host': '127.0.0.1',
            'port': 8080,
            'path': 'metrics',
        })
        return config

    def collect(self):
        if json is None:
            self.log.error('Unable to import json')
            return {}
        url = 'http://%s:%i/metrics' % (
            self.config['host'], int(self.config['port']))
        try:
            response = urllib2.urlopen(url)
        except urllib2.HTTPError, err:
            self.log.error("%s: %s", url, err)
            return

        try:
            metrics = json.load(response)
        except (TypeError, ValueError):
            self.log.error("Unable to parse response from springboot as a json object")
            return

        for key in metrics:
            self.log.debug("publishing metric: %s", key)
            self.publish(key, metrics[key])
