# coding=utf-8

"""
Collects data from php-fpm if the
[pm.status_path](https://secure.php.net/manual/en/install.fpm.configuration.php#pm.status-path)
is enabled in php-fpm configuration


#### Usage

A sample php-fpm config for this collector to work is

```
pm.status_path = /fpm-status
```

If the URL of the fpm-status page is http://127.0.0.1:8080/fpm-status, you
need to set:

```
enabled = True
host = 127.0.0.1
port = 8080
uri = fpm-status
```

#### Dependencies

 * json (or simplejson)

"""

try:
    import json
except ImportError:
    import simplejson as json

import diamond.collector
import diamond.pycompat


class PhpFpmCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(PhpFpmCollector, self).get_default_config_help()
        config_help.update({
            'uri': 'Path part of the URL, with or without the leading /',
            'host': 'Host part of the URL',
            'port': 'Port part of the URL',
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
            response = diamond.pycompat.urlopen("http://%s:%s/%s?json" % (
                self.config['host'], int(self.config['port']),
                self.config['uri']))
        except Exception as e:
            self.log.error('Couldnt connect to php-fpm status page: %s', e)
            return {}

        try:
            j = json.loads(response.read())
        except Exception as e:
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
