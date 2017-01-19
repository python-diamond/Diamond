<!--This file was generated from the python source
Please edit the source to make changes
-->
DseOpsCenterCollector
=====

Collect the DataStax OpsCenter metrics

#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
cluster_id |  | Set cluster ID/name.<br>
 | 
default_tail_opts | &forecast=0&node_aggregation=1 | Chaning these is not recommended. | str
enabled | False | Enable collecting these metrics | bool
host | 127.0.0.1 |  | str
measure_collector_time | False | Collect the collector run time in ms | bool
metrics | cf-bf-false-positives,cf-bf-false-ratio,cf-bf-space-used,cf-keycache-hit-rate,cf-keycache-hits,cf-keycache-requests,cf-live-disk-used,cf-live-sstables,cf-pending-tasks,cf-read-latency-op,cf-read-ops,cf-rowcache-hit-rate,cf-rowcache-hits,cf-rowcache-requests,cf-total-disk-used,cf-write-latency-op,cf-write-ops,cms-collection-count,cms-collection-time,data-load,heap-committed,heap-max,heap-used,key-cache-hit-rate,key-cache-hits,key-cache-requests,nonheap-committed,nonheap-max,nonheap-used,pending-compaction-tasks,pending-flush-sorter-tasks,pending-flushes,pending-gossip-tasks,pending-hinted-handoff,pending-internal-responses,pending-memtable-post-flushers,pending-migrations,pending-misc-tasks,pending-read-ops,pending-read-repair-tasks,pending-repair-tasks,pending-repl-on-write-tasks,pending-request-responses,pending-streams,pending-write-ops,read-latency-op,read-ops,row-cache-hit-rate,row-cache-hits,row-cache-requests,solr-avg-time-per-req,solr-errors,solr-requests,solr-timeouts,total-bytes-compacted,total-compactions-completed,write-latency-op,write-ops | You can list explicit metrics if you like,<br>
 by default all know metrics are included.<br>
 | str
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
node_group | * | Set node group name, any by default<br>
 | str
port | 8888 |  | int

#### Example Output

```
servers.hostname.cassandra.cf-bf-false-positives.dse_system.leases 0
servers.hostname.cassandra.key-cache-hits 9.11431694527
servers.hostname.cassandra.key-cache-requests 38.2884782205
servers.hostname.cassandra.nonheap-max 136314880
servers.hostname.cassandra.nonheap-used 48491696.6667
servers.hostname.cassandra.read-ops 55.9152622223
```

