# coding=utf-8

"""

Collects metrics from an Etcd instance.

#### Example Configuration

```
    host = localhost
    port = 2379
```
"""

import diamond.collector
import json
import urllib2

METRICS_KEYS = ['sendPkgRate',
                'recvPkgRate',
                'sendAppendRequestCnt',
                'recvAppendRequestCnt',
                'sendBandwidthRate',
                'recvBandwidthRate']


class EtcdCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(EtcdCollector,
                            self).get_default_config_help()
        config_help.update({
            'host': 'Hostname',
            'port': 'Port (default is 2379)',
            'timeout': 'Timeout per HTTP(s) call',
            'use_tls': 'Use TLS/SSL or just unsecure (default is unsecure)',
            'ca_file': 'Only applies when use_tls=true. Path to CA certificate'
                       ' file to use for server identity verification',
        })
        return config_help

    def get_default_config(self):
        config = super(EtcdCollector, self).get_default_config()
        config.update({
            'host': 'localhost',
            'port': 2379,
            'path': 'etcd',
            'timeout': 5,
            'use_tls': False,
            'ca_file': '',
        })
        return config

    def __init__(self, *args, **kwargs):
        super(EtcdCollector, self).__init__(*args, **kwargs)

    def collect(self):
        self.collect_self_metrics()
        self.collect_store_metrics()

    def collect_self_metrics(self):
        metrics = self.get_self_metrics()

        if 'state' in metrics and metrics['state'] == "StateLeader":
            self.publish("self.is_leader", 1)
        else:
            self.publish("self.is_leader", 0)

        for k in METRICS_KEYS:
            if k not in metrics:
                continue
            v = metrics[k]
            key = self.clean_up(k)
            self.publish("self.%s" % key, v)

    def collect_store_metrics(self):
        metrics = self.get_store_metrics()

        for k, v in metrics.iteritems():
            key = self.clean_up(k)
            self.publish("store.%s" % key, v)

    def get_self_metrics(self):
        return self.get_metrics("self")

    def get_store_metrics(self):
        return self.get_metrics("store")

    def get_metrics(self, category):
        try:
            opts = {
                'timeout': int(self.config['timeout']),
            }
            if self.config['use_tls']:
                protocol = "https"
                opts['cafile'] = self.config['ca_file']
            else:
                protocol = "http"

            url = "%s://%s:%s/v2/stats/%s" % (protocol, self.config['host'],
                                              self.config['port'], category)

            return json.load(urllib2.urlopen(url, **opts))
        except (urllib2.HTTPError, ValueError), err:
            self.log.error('Unable to read JSON response: %s' % err)
            return {}

    def clean_up(self, text):
        return text.replace('/', '.')
