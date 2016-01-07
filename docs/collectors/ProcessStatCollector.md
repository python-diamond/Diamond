<!--This file was generated from the python source
Please edit the source to make changes
-->
ProcessStatCollector
=====

The ProcessStatCollector collects metrics on process stats from
/proc/stat

#### Dependencies

 * /proc/stat


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
servers.hostname.proc.btime 1319181102
servers.hostname.proc.ctxt 1791
servers.hostname.proc.processes 2
servers.hostname.proc.procs_blocked 0
servers.hostname.proc.procs_running 1
```

