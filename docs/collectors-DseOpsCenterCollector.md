DseOpsCenterCollector
=====

Collect the DataStax OpsCenter metrics

#### Dependencies

 * urlib2


#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>byte_unit</td><td>byte</td><td>Default numeric output(s)</td><td>str</td></tr>
<tr><td>cluster_id</td><td></td><td>Set cluster ID/name.<br>
</td><td></td></tr>
<tr><td>default_tail_opts</td><td>&forecast=0&node_aggregation=1</td><td>Chaning these is not recommended.</td><td>str</td></tr>
<tr><td>enabled</td><td>False</td><td>Enable collecting these metrics</td><td>bool</td></tr>
<tr><td>host</td><td>127.0.0.1</td><td></td><td>str</td></tr>
<tr><td>measure_collector_time</td><td>False</td><td>Collect the collector run time in ms</td><td>bool</td></tr>
<tr><td>metrics</td><td>cf-bf-false-positives,cf-bf-false-ratio,cf-bf-space-used,cf-keycache-hit-rate,cf-keycache-hits,cf-keycache-requests,cf-live-disk-used,cf-live-sstables,cf-pending-tasks,cf-read-latency-op,cf-read-ops,cf-rowcache-hit-rate,cf-rowcache-hits,cf-rowcache-requests,cf-total-disk-used,cf-write-latency-op,cf-write-ops,cms-collection-count,cms-collection-time,data-load,heap-committed,heap-max,heap-used,key-cache-hit-rate,key-cache-hits,key-cache-requests,nonheap-committed,nonheap-max,nonheap-used,pending-compaction-tasks,pending-flush-sorter-tasks,pending-flushes,pending-gossip-tasks,pending-hinted-handoff,pending-internal-responses,pending-memtable-post-flushers,pending-migrations,pending-misc-tasks,pending-read-ops,pending-read-repair-tasks,pending-repair-tasks,pending-repl-on-write-tasks,pending-request-responses,pending-streams,pending-write-ops,read-latency-op,read-ops,row-cache-hit-rate,row-cache-hits,row-cache-requests,solr-avg-time-per-req,solr-errors,solr-requests,solr-timeouts,total-bytes-compacted,total-compactions-completed,write-latency-op,write-ops</td><td>You can list explicit metrics if you like,<br>
 by default all know metrics are included.<br>
</td><td>str</td></tr>
<tr><td>metrics_blacklist</td><td>None</td><td>Regex to match metrics to block. Mutually exclusive with metrics_whitelist</td><td>NoneType</td></tr>
<tr><td>metrics_whitelist</td><td>None</td><td>Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist</td><td>NoneType</td></tr>
<tr><td>node_group</td><td>*</td><td>Set node group name, any by default<br>
</td><td>str</td></tr>
<tr><td>port</td><td>8888</td><td></td><td>int</td></tr>
</table>

#### Example Output

```
servers.hostname.cassandra.cf-bf-false-positives.dse_system.leases 0
servers.hostname.cassandra.key-cache-hits 9.11431694527
servers.hostname.cassandra.key-cache-requests 38.2884782205
servers.hostname.cassandra.nonheap-max 136314880
servers.hostname.cassandra.nonheap-used 48491696.6667
servers.hostname.cassandra.read-ops 55.9152622223
```

### This file was generated from the python source
### Please edit the source to make changes

