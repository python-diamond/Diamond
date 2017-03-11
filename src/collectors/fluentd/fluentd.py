# coding=utf-8

"""
The FlutendCollector monitors fluentd and data about the kinesis stream.

#### Dependencies

 * flutend

#### Example config

```
    enabled = True
    host = localhost
    port = 24220
    [[[collect]]]
    kinesis = buffer_queue_length, buffer_total_queued_size, retry_count
```

"""

import diamond.collector
import diamond.pycompat
import json


class FluentdCollector(diamond.collector.Collector):

    API_PATH = '/api/plugins.json'

    def get_default_config_help(self):
        config_help = super(FluentdCollector, self).get_default_config_help()
        config_help.update({
            'host': 'Fluentd host',
            'port': 'Fluentd port',
            'collect': 'Plugins and their metrics to collect'
        })
        return config_help

    def get_default_config(self):
        config = super(FluentdCollector, self).get_default_config()
        config.update({
            'host': 'localhost',
            'port': '24220',
            'path': 'fluentd',
            'collect': {}
        })
        return config

    def collect(self):
        params = (self.config['host'], self.config['port'], self.API_PATH)
        url = "http://%s:%s/%s" % params

        res = diamond.pycompat.urlopen(url)
        data = json.load(res)

        result = self.parse_api_output(data)
        for r in result:
            self.publish(r[0], r[1])

    def parse_api_output(self, status):
        result = []
        for p in status.get('plugins'):
            if p['type'] in self.config['collect'].keys():
                for m in self.config['collect'].get(p['type']):
                    tag = ".".join([p['type'], m])
                    result.append((tag, p.get(m)))
        return result
