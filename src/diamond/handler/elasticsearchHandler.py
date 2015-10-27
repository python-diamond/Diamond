# coding=utf-8

"""
Send metrics to an
[ElasticSearch](https://www.elastic.co/products/elasticsearch) cluster.

ElasticSearch is an easily scalable database with a REST/JSON API. It has
been used for log storage and analysis and now for metrics as well!

ElasticSearch has introduced the
[Beats](https://www.elastic.co/products/beats) library to ship various metrics
to ES. This handler is Beats compatible.

#### Dependencies

  * elasticsearch python module (pip install elasticsearch)

#### Setup

1. Decide what to call the index the metrics will be saved in. By default
the handler follows the statsd and beats tradition and creates daily indices
called "diamond-YYYY.MM.DD". Kibana, the most common graphical interface
to ElasticSearch has built-in support for this.

2. Decide if you want to change the default field names.

2. Load a default template into ES to define the fields and options:

```
curl -XPUT localhost:9200/_template/diamond-template -d '
{
  "template": "diamond-*",
  "mappings": {
    "_default_": {
      "_all": {
        "enabled": false
      },
      "dynamic_templates": [
        {
          "template1": {
            "mapping": {
              "doc_values": true,
              "ignore_above": 1024,
              "index": "not_analyzed",
              "type": "{dynamic_type}"
            },
            "match": "*"
          }
        }
      ],
      "properties": {
        "timestamp": {
          "type": "date"
        }
      }
    }
  },
  "settings": {
    "index.refresh_interval": "5s"
  }
}'
```

4. Add the ElasticSearchHandler config to the diamond.conf handlers section:
(minimum config shown)

```
handlers = diamond.handler.elasticsearchHandler.ElasticSearchHandler

[handlers]

[[ElasticSearchHandler]]
host_urls = http://127.0.0.1:9200/
```

#### Acknowledgements

ElasticSearchHandler was made possible by [ACT.md](http://act.md)

"""

__author__ = 'imre Fitos'
__version__ = '1.0'

import collections
import time
from Handler import Handler

try:
    from elasticsearch import Elasticsearch, helpers
except ImportError:
    Elasticsearch = None


class ElasticSearchHandler(Handler):

    def __init__(self, *args, **kwargs):
        super(ElasticSearchHandler, self).__init__(*args, **kwargs)

        if Elasticsearch is None:
            self.log.error(
                'Failed to import elasticsearch module. Handler disabled')
            self.enabled = False
            return
        # attempt to connect
        try:
            url_list = []
            for host in self.config['host_urls'].split(','):
                url_list.append(host)
            self.es = Elasticsearch(url_list)
        except Exception as exc:
            self.log.error("ElasticSearchHandler start failed: {}".format(exc))
            self.enabled = False
        # save options into vars
        self.doc_type = self.config.get('doc_type')
        self.batch_size = self.config.get('batch_size')
        self.flush_seconds = int(self.config.get('flush_seconds'))
        self.index_format = self.config.get('index_format')
        self.timestamp_field = self.config.get('timestamp_field')
        self.host_field = self.config.get('host_field')
        self.collector_field = self.config.get('collector_field')

        self.queue = collections.deque([])
        self.flush_time = time.time()
        self.last_timestamp = 0

        self.log.debug("ElasticSearchHandler initialized.")

    def get_default_config_help(self):
        config = super(ElasticSearchHandler, self).get_default_config_help()
        config.update({
            'host_urls': "ElasticSearch server URLs separated by commas",
            'batch_size': "Max number of metrics to send in one batch",
            'flush_seconds': "Max seconds between writes to server",
            'index_format':
                "What to name indices (default 'diamond-YYYY.MM.DD')",
            'timestamp_field':
                "Field used for timestamp (default 'timestamp')",
            'host_field': "Field used for host name (default 'shipper')",
            'collector_field':
                "Field used for collector name (default 'type')",
            'doc_type': "document type in ES index (default 'metric')"
        })
        return config

    def get_default_config(self):
        config = super(ElasticSearchHandler, self).get_default_config()
        config.update({
            'host_urls': 'http://127.0.0.1:9200/',
            'doc_type': 'metric',
            'batch_size': 1000,
            'flush_seconds': 10,
            'index_format': 'diamond-%Y.%m.%d',
            'timestamp_field': 'timestamp',
            'host_field': 'shipper',
            'collector_field': 'type'
        })
        return config

    def process(self, metric):
        """Take single metric from main Diamond process"""
        if not self.enabled:
            return
        # only flush when a new batch is starting
        # so we don't end up with partial metrics
        if metric.timestamp != self.last_timestamp:
            if time.time() > self.flush_time + self.flush_seconds or \
                    len(self.queue) > self.batch_size:
                self.flush_time = time.time()
                self.flush()
            self.last_timestamp = metric.timestamp
        # save new metric after flushing last batch
        self.queue.append(metric)

    def flush(self):
        """Write all metrics to ES server"""
        if not self.enabled:
            return
        if len(self.queue) == 0:
            return
        actions = []
        action = None
        current_timestamp = 0
        current_collector = ''
        current_host = ''
        while len(self.queue) > 0:
            metric = self.queue.popleft()
            if (metric.timestamp != current_timestamp or
                    metric.getCollectorPath() != current_collector or
                    metric.host != current_host):
                # create empty action document
                current_timestamp = metric.timestamp
                current_collector = metric.getCollectorPath()
                current_host = metric.host
                if action is not None:
                    actions.append(action)
                action = {
                    '_type': self.doc_type,
                    '_source': {
                        self.timestamp_field: metric.timestamp * 1000,
                        self.host_field: metric.host,
                        'type': metric.getCollectorPath(),
                        'count': 1,
                        current_collector: {}
                    }
                }
            # merge new metric into the action structure
            partialaction = action['_source'][current_collector]
            position = 3
            length = len(metric.path.split('.')) - 1
            for portion in metric.path.split('.')[3:]:
                if not partialaction.get(str(portion)):
                    if position == length:
                        # we are at the final json field, save value
                        partialaction[str(portion)] = metric.value
                    else:
                        partialaction[str(portion)] = {}
                position += 1
                partialaction = partialaction[str(portion)]

        if action is not None:
            actions.append(action)

        if len(actions) > 0:
            try:
                result = helpers.bulk(
                    client=self.es,
                    index=time.strftime(
                        self.index_format, time.localtime(self.flush_time)
                    ),
                    actions=actions,
                    stats_only=True
                )
                self.log.debug(
                    "ElasticSearchHandler docs written: {}, writes failed: {}"
                        .format(result[0], result[1]))
            except Exception as exc:
                self._throttle_error("ElasticSearchHandler: {}".format(exc))
