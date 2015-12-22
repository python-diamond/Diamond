<!--This file was generated from the python source
Please edit the source to make changes
-->
EndecaDgraphCollector
=====

Collects stats from Endeca Dgraph/MDEX server.
Tested with: Endeca Information Access Platform version 6.3.0.655584

=== Authors

Jan van Bemmelen <jvanbemmelen@bol.com>
Renzo Toma <rtoma@bol.com>


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
host | localhost | Hostname of Endeca Dgraph instance | str
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
port | 8080 | Port of the Dgraph API listener | int
timeout | 1 | Timeout for http API calls | int

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

