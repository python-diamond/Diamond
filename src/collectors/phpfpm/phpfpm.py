# coding=utf-8

"""
Collects data from php-fpm if the pm.status_path is enabled

A sample php-fpm config for this collector to work is

pm.status_path = /fpm-status


#### Dependencies

 * urllib2
 * json (or simeplejson)

"""

try:
    import json

    json  # workaround for pyflakes issue #13
except ImportError:
    import simplejson as json

import urllib2
import diamond.collector


class PhpFpmCollector(diamond.collector.Collector):
    def get_default_config_help(self):
        config_help = super(PhpFpmCollector, self).get_default_config_help()
        config_help.update({
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(PhpFpmCollector, self).get_default_config()
        config.update({
            'host': 'localhost',
            'port': 80,
            'uri': 'fpm-status',
            'byte_unit': ['byte'],
        })
        return config

    def collect(self):
        #
        # if there is a / in front remove it
        if self.config['uri'][0] == '/':
            self.config['uri'] = self.config['uri'][1:]

        try:
            response = urllib2.urlopen("http://%s:%s/%s" % (
                self.config['host'], int(self.config['port']), 
                self.config['uri']))
        except Exception, e:
            self.log.error('Couldnt connect to php-fpm status page: %s', e)
            return {}

        try:
            j = json.loads(response.read())
        except Exception, e:
            self.log.error('Couldnt parse json: %s', e)
            return {}

        for k,v in j.items():
            #
            # php-fpm has spaces in the keys so lets replace all spaces with _
            k = k.replace(" ", "_")

            self.publish(k, v)
