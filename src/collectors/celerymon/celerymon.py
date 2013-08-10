# coding=utf-8

"""
Collects simple task stats out of a running celerymon process

#### Dependencies

 * celerymon connected to celery broker

Example config file CelerymonCollector.conf

```
enabled=True
host=celerymon.example.com
port=16379
```

"""

import diamond.collector
import json
import urllib2
import time


class CelerymonCollector(diamond.collector.Collector):

    LastCollectTime = None

    def get_default_config_help(self):
        config_help = super(CelerymonCollector, self).get_default_config_help()
        config_help.update({
            'path': 'celerymon',
            'host': 'A single hostname to get metrics from',
            'port': 'The celerymon port'

        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(CelerymonCollector, self).get_default_config()
        config.update({
            'host':     'localhost',
            'port':     '8989'
        })
        return config

    def collect(self):
        """
        Overrides the Collector.collect method
        """

        # Handle collection time intervals correctly
        CollectTime = int(time.time())
        time_delta = float(self.config['interval'])
        if not self.LastCollectTime:
            self.LastCollectTime = CollectTime - time_delta

        host = self.config['host']
        port = self.config['port']

        celerymon_url = "http://%s:%s/api/task/?since=%i" % (
            host, port, self.LastCollectTime)
        response = urllib2.urlopen(celerymon_url)
        body = response.read()
        celery_data = json.loads(body)

        results = dict()
        total_messages = 0
        for data in celery_data:
            name = str(data[1]['name'])
            if name not in results:
                results[name] = dict()
            state = str(data[1]['state'])
            if state not in results[name]:
                results[name][state] = 1
            else:
                results[name][state] += 1
            total_messages += 1

        # Publish Metric
        self.publish('total_messages', total_messages)
        for result in results:
            for state in results[result]:
                metric_value = results[result][state]
                metric_name = "%s.%s" % (result, state)
                self.publish(metric_name, metric_value)

        self.LastCollectTime = CollectTime
