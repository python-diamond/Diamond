<!--This file was generated from the python source
Please edit the source to make changes
-->
NetstatCollector
=====

The NetstatCollector class collects metrics on number of connections
in each state

#### Dependencies

 * /proc/net/tcp

Based on Ricardo Pascal's "netstat in <100 lines of code"


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
__EXAMPLESHERE__
```

