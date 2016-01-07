<!--This file was generated from the python source
Please edit the source to make changes
-->
ElasticSearchCollector
=====

Collect the elasticsearch stats for the local node.

Supports multiple instances. When using the 'instances'
parameter the instance alias will be appended to the
'path' parameter.

#### Dependencies

 * urlib2


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
host | 127.0.0.1 |  | str
instances | , | List of instances. When set this overrides the 'host' and 'port' settings. Instance format: instance [<alias>@]<hostname>[:<port>] | list
logstash_mode | False | If 'indices' stats are gathered, remove the YYYY.MM.DD suffix from the index name (e.g. logstash-adm-syslog-2014.01.03) and use that as a bucket for all 'day' index stats. | bool
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
port | 9200 |  | int
stats | jvm, thread_pool, indices, | Available stats:<br>
 - jvm (JVM information)<br>
 - thread_pool (Thread pool information)<br>
 - indices (Individual index stats)<br>
 | list

#### Example Output

```
servers.hostname.elasticsearch.cache.filter.evictions 9
servers.hostname.elasticsearch.cache.filter.size 1700
servers.hostname.elasticsearch.cache.id.size 98
servers.hostname.elasticsearch.fielddata.evictions 12
servers.hostname.elasticsearch.fielddata.size 1448
```

