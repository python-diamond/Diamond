# coding=utf-8

"""
Collects data from php-fpm if the pm.status_path is enabled


#### Usage

A sample php-fpm config for this collector to work is

```
pm.status_path = /fpm-status
```

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
            'path': 'phpfpm',
        })
        return config

    def collect(self):
        #
        # if there is a / in front remove it
        if self.config['uri'][0] == '/':
            self.config['uri'] = self.config['uri'][1:]

        try:
            response = urllib2.urlopen("http://%s:%s/%s?json" % (
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

        valid_metrics = [
            'accepted_conn',
            'listen_queue',
            'max_listen_queue',
            'listen_queue_len',
            'idle_processes',
            'active_processes',
            'total_processes',
            'max_active_processes',
            'max_children_reached',
            'slow_requests'
        ]
        for k, v in j.items():
            #
            # php-fpm has spaces in the keys so lets replace all spaces with _
            k = k.replace(" ", "_")

            if k in valid_metrics:
                self.publish(k, v)
