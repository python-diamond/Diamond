<!--This file was generated from the python source
Please edit the source to make changes
-->
SoftInterruptCollector
=====

The SoftInterruptCollector collects metrics on software interrupts from
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
servers.hostname.softirq.0 0
servers.hostname.softirq.1 1729
servers.hostname.softirq.2 2
servers.hostname.softirq.3 240
servers.hostname.softirq.4 31
servers.hostname.softirq.5 0
servers.hostname.softirq.6 0
servers.hostname.softirq.7 1480
servers.hostname.softirq.8 0
servers.hostname.softirq.9 1489
servers.hostname.softirq.total 4971
```

