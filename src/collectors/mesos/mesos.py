# coding=utf-8

"""
Collect the Mesos stats for the local node.

#### Dependencies
 * urlib2
"""

import urllib2

try:
    import json
except ImportError:
    import simplejson as json

import diamond.collector


class MesosCollector(diamond.collector.Collector):
    def get_default_config_help(self):
        config_help = super(MesosCollector,
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
        config = super(MesosCollector, self).get_default_config()
        config.update({
            'host': '127.0.0.1',
            'port': 5050,
            'path': 'metrics/snapshot',
        })
        return config

    def _get(self, host, port, path):
        """
        Execute a Marathon API call.
        """
        url = 'http://%s:%s/%s' % (host, port, path)
        try:
            response = urllib2.urlopen(url)
        except Exception, err:
            self.log.error("%s: %s", url, err)
            return False

        try:
            doc = json.load(response)
        except (TypeError, ValueError):
            self.log.error("Unable to parse response from Mesos as a"
                           + " json object")
            return False

        return doc

    def collect(self):
        if json is None:
            self.log.error('Unable to import json')
            return {}

        result = self._get(
            self.config['host'],
            self.config['port'],
            self.config['path']
        )
        if not result:
            return

        for key in result:
            value = result[key]
            metric = key.replace('/', '.')
            self.publish(metric, value, precision=self._precision(value))

    def _precision(self, value):
        """
        Return the precision of the number
        """
        value = str(value)
        decimal = value.rfind('.')
        if decimal == -1:
            return 0
        return len(value) - decimal - 1
