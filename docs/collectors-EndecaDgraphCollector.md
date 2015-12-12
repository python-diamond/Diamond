EndecaDgraphCollector
=====

Collects stats from Endeca Dgraph/MDEX server.
Tested with: Endeca Information Access Platform version 6.3.0.655584

=== Authors

Jan van Bemmelen <jvanbemmelen@bol.com>
Renzo Toma <rtoma@bol.com>


#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>byte_unit</td><td>byte</td><td>Default numeric output(s)</td><td>str</td></tr>
<tr><td>enabled</td><td>False</td><td>Enable collecting these metrics</td><td>bool</td></tr>
<tr><td>host</td><td>localhost</td><td>Hostname of Endeca Dgraph instance</td><td>str</td></tr>
<tr><td>measure_collector_time</td><td>False</td><td>Collect the collector run time in ms</td><td>bool</td></tr>
<tr><td>metrics_blacklist</td><td>None</td><td>Regex to match metrics to block. Mutually exclusive with metrics_whitelist</td><td>NoneType</td></tr>
<tr><td>metrics_whitelist</td><td>None</td><td>Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist</td><td>NoneType</td></tr>
<tr><td>port</td><td>8080</td><td>Port of the Dgraph API listener</td><td>int</td></tr>
<tr><td>timeout</td><td>1</td><td>Timeout for http API calls</td><td>int</td></tr>
</table>

#### Example Output

```
servers.hostname.endeca.dgraph.statistics.cache_section.main_cache.aggregatedrecordcount.entry_count 3957
servers.hostname.endeca.dgraph.statistics.cache_section.main_cache.dval_bincount.entry_count 4922448
servers.hostname.endeca.dgraph.statistics.hot_spot_analysis.content_spotlighting_performance.min 0.0209961
servers.hostname.endeca.dgraph.statistics.hot_spot_analysis.insertion_sort_time.avg 0.00523964
servers.hostname.endeca.dgraph.statistics.hot_spot_analysis.ordinal_insertion_sort_time.n 1484793
servers.hostname.endeca.dgraph.statistics.search_performance_analysis.qconj_lookupphr.min 0.000976562
servers.hostname.endeca.dgraph.statistics.updates.update_latency.commit.audit_stat_calculation_time_resume_.n 0
```

### This file was generated from the python source
### Please edit the source to make changes

