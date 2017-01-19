<!--This file was generated from the python source
Please edit the source to make changes
-->
NumaCollector
=====

This class collects data on NUMA utilization

#### Dependencies

* numactl


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType

#### Example Output

```
servers.hostname.numa.node_0_free_MB 342
servers.hostname.numa.node_0_size_MB 15976
```

