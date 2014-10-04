# coding=utf-8

"""
Collects data form sidekiq web

#### Dependencies

 * urllib2
 * json (or simeplejson)

"""

try:
    import json
except ImportError:
    import simplejson as json

import urllib2
import diamond.collector


class SidekiqWebCollector(diamond.collector.Collector):
    def get_default_config_help(self):
        config_help = super(SidekiqWebCollector, self).get_default_config_help()
        config_help.update({
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(SidekiqWebCollector, self).get_default_config()
        config.update({
            'host': 'localhost',
            'port': 9999,
            'byte_unit': ['byte'],
        })
        return config

    def collect(self):
        try:
            response = urllib2.urlopen("http://%s:%s/dashboard/stats" % (
                self.config['host'], int(self.config['port'])))
        except Exception, e:
            self.log.error('Couldnt connect to sidekiq-web: %s', e)
            return {}

        try:
            j = json.loads(response.read())
        except Exception, e:
            self.log.error('Couldnt parse json: %s', e)
            return {}

        for k in j:
            for item, value in j[k].items():

                if isinstance(value, (str, unicode)) and 'M' in value:
                    value = float(value.replace('M', ''))
                    for unit in self.config['byte_unit']:
                        unit_value = diamond.convertor.binary.convert(
                            value=value,
                            oldUnit='megabyte',
                            newUnit=unit)

                        self.publish("%s.%s_%s" % (k, item, unit), unit_value)
                else:
                    self.publish("%s.%s" % (k, item), value)
