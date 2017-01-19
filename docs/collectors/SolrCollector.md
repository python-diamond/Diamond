<!--This file was generated from the python source
Please edit the source to make changes
-->
SolrCollector
=====

Collect the solr stats for the local node

#### Dependencies

 * posixpath
 * urllib2
 * json


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
core | None | Which core info should collect (default: all cores) | NoneType
enabled | False | Enable collecting these metrics | bool
host | localhost |  | str
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
port | 8983 |  | int
stats | jvm, core, response, query, update, cache, | Available stats: <br>
 - core (Core stats)<br>
 - response (Ping response stats)<br>
 - query (Query Handler stats)<br>
 - update (Update Handler stats)<br>
 - cache (fieldValue, filter, document & queryResult cache stats)<br>
 - jvm (JVM information) <br>
 | list

#### Example Output

```
servers.hostname.cache.documentCache.cumulative_evictions 0
servers.hostname.cache.documentCache.cumulative_hitratio 0.0
servers.hostname.cache.documentCache.cumulative_hits 0
servers.hostname.cache.documentCache.cumulative_inserts 0
servers.hostname.cache.documentCache.cumulative_lookups 0
servers.hostname.cache.documentCache.evictions 0
servers.hostname.cache.documentCache.hitratio 0.0
servers.hostname.cache.documentCache.hits 0
servers.hostname.cache.documentCache.inserts 0
servers.hostname.cache.documentCache.lookups 0
servers.hostname.cache.documentCache.size 0
servers.hostname.cache.documentCache.warmupTime 0
servers.hostname.cache.fieldValueCache.cumulative_evictions 0
servers.hostname.cache.fieldValueCache.cumulative_hitratio 0.0
servers.hostname.cache.fieldValueCache.cumulative_hits 0
servers.hostname.cache.fieldValueCache.cumulative_inserts 0
servers.hostname.cache.fieldValueCache.cumulative_lookups 0
servers.hostname.cache.fieldValueCache.evictions 0
servers.hostname.cache.fieldValueCache.hitratio 0.0
servers.hostname.cache.fieldValueCache.hits 0
servers.hostname.cache.fieldValueCache.inserts 0
servers.hostname.cache.fieldValueCache.lookups 0
servers.hostname.cache.fieldValueCache.size 0
servers.hostname.cache.fieldValueCache.warmupTime 0
servers.hostname.cache.filterCache.cumulative_evictions 0
servers.hostname.cache.filterCache.cumulative_hitratio 0.0
servers.hostname.cache.filterCache.cumulative_hits 0
servers.hostname.cache.filterCache.cumulative_inserts 0
servers.hostname.cache.filterCache.cumulative_lookups 0
servers.hostname.cache.filterCache.evictions 0
servers.hostname.cache.filterCache.hitratio 0.0
servers.hostname.cache.filterCache.hits 0
servers.hostname.cache.filterCache.inserts 0
servers.hostname.cache.filterCache.lookups 0
servers.hostname.cache.filterCache.size 0
servers.hostname.cache.filterCache.warmupTime 0
servers.hostname.cache.queryResultCache.cumulative_evictions 0
servers.hostname.cache.queryResultCache.cumulative_hitratio 0.66
servers.hostname.cache.queryResultCache.cumulative_hits 2
servers.hostname.cache.queryResultCache.cumulative_inserts 1
servers.hostname.cache.queryResultCache.cumulative_lookups 3
servers.hostname.cache.queryResultCache.evictions 0
servers.hostname.cache.queryResultCache.hitratio 0.66
servers.hostname.cache.queryResultCache.hits 2
servers.hostname.cache.queryResultCache.inserts 1
servers.hostname.cache.queryResultCache.lookups 3
servers.hostname.cache.queryResultCache.size 1
servers.hostname.cache.queryResultCache.warmupTime 0
servers.hostname.core.maxDoc 321
servers.hostname.core.numDocs 184
servers.hostname.core.warmupTime 0
servers.hostname.jvm.mem.free 42.7
servers.hostname.jvm.mem.max 185.6
servers.hostname.jvm.mem.total 61.9
servers.hostname.jvm.mem.used 19.2
servers.hostname.queryhandler.standard.avgRequestsPerSecond 0.00016776958
servers.hostname.queryhandler.standard.avgTimePerRequest 90
servers.hostname.queryhandler.standard.errors 0
servers.hostname.queryhandler.standard.requests 3
servers.hostname.queryhandler.standard.timeouts 0
servers.hostname.queryhandler.standard.totalTime 270
servers.hostname.queryhandler.update.avgRequestsPerSecond 0
servers.hostname.queryhandler.update.errors 0
servers.hostname.queryhandler.update.requests 0
servers.hostname.queryhandler.update.timeouts 0
servers.hostname.queryhandler.update.totalTime 0
servers.hostname.response.QueryTime 5
servers.hostname.response.Status 0
servers.hostname.updatehandler.adds 0
servers.hostname.updatehandler.autocommits 0
servers.hostname.updatehandler.commits 0
servers.hostname.updatehandler.cumulative_adds 0
servers.hostname.updatehandler.cumulative_errors 0
servers.hostname.updatehandler.docsPending 0
servers.hostname.updatehandler.errors 0
servers.hostname.updatehandler.optimizes 0
servers.hostname.updatehandler.rollbacks 0
```

