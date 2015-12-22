<!--This file was generated from the python source
Please edit the source to make changes
-->
VMStatCollector
=====

Uses /proc/vmstat to collect data on virtual memory manager

#### Dependencies

 * /proc/vmstat


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
servers.hostname.vmstat.pgpgin 0.0
servers.hostname.vmstat.pgpgout 9.2
servers.hostname.vmstat.pswpin 0.0
servers.hostname.vmstat.pswpout 0.0
```

