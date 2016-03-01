<!--This file was generated from the python source
Please edit the source to make changes
-->
LoadAverageCollector
=====

Uses /proc/loadavg to collect data on load average

#### Dependencies

 * /proc/loadavg


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
simple | False | Only collect the 1 minute load average | str

#### Example Output

```
servers.hostname.loadavg.01 (0.12, 2)
servers.hostname.loadavg.05 (0.23, 2)
servers.hostname.loadavg.15 (0.34, 2)
servers.hostname.loadavg.processes_running 1
servers.hostname.loadavg.processes_total 235
```

