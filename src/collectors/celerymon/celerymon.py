# coding=utf-8

"""
Collects simple task stats out of a running celerymon process

#### Dependencies

 * celerymon connected to celery broker

#### Customizing a collector



Example config file CelerymonCollector.conf

```
enabled=True
host=redis.example.com
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
        config_help = super(MongoDBCollector, self).get_default_config_help()
        config_help.update({
            'host': 'A single hostname to get metrics from'
            'port': 'The celerymon port',

        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(ExampleCollector, self).get_default_config()
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

        celerymon_url = "http://%s:%s/api/task/?since=%s" % (host, port, self.LastCollectTime)
        response  = urllib2.urlopen(celerymon_url)
        body = response.read()
        celery_data = json.loads(body)

        results = dict()
        results = ['total_messages'] - 0
        for data in celery_data:
            name = str(data[1]['name'])
            if name not in results:
                results[name] = dict()
            state = str(data[1]['state'])
            if state no in results[name]:
                results[name][state] = 1
            else:
                results[name][state] += 1
            results['total_messages'] += 1

        # Publish Metric
        for result in results:
            for state in results[result]:
                metric_value = results[result][state]
                metric_name = "%s.%s" % (result, state)
                self.publish(metric_name, metric_value)


        self.LastCollectTime = CollectTime
