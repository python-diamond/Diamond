SolrCollector
=====

Collect the solr stats for the local node

#### Dependencies

 * posixpath
 * urllib2
 * json


#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>byte_unit</td><td>byte</td><td>Default numeric output(s)</td><td>str</td></tr>
<tr><td>core</td><td>None</td><td>Which core info should collect (default: all cores)</td><td>NoneType</td></tr>
<tr><td>enabled</td><td>False</td><td>Enable collecting these metrics</td><td>bool</td></tr>
<tr><td>host</td><td>localhost</td><td></td><td>str</td></tr>
<tr><td>measure_collector_time</td><td>False</td><td>Collect the collector run time in ms</td><td>bool</td></tr>
<tr><td>metrics_blacklist</td><td>None</td><td>Regex to match metrics to block. Mutually exclusive with metrics_whitelist</td><td>NoneType</td></tr>
<tr><td>metrics_whitelist</td><td>None</td><td>Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist</td><td>NoneType</td></tr>
<tr><td>port</td><td>8983</td><td></td><td>int</td></tr>
<tr><td>stats</td><td>jvm, core, response, query, update, cache,</td><td>Available stats: <br>
 - core (Core stats)<br>
 - response (Ping response stats)<br>
 - query (Query Handler stats)<br>
 - update (Update Handler stats)<br>
 - cache (fieldValue, filter, document & queryResult cache stats)<br>
 - jvm (JVM information) <br>
</td><td>list</td></tr>
</table>

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

### This file was generated from the python source
### Please edit the source to make changes

