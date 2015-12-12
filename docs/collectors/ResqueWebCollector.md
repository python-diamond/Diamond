<!--This file was generated from the python source
Please edit the source to make changes
-->
ResqueWebCollector
=====

Collects data for Resque Web

#### Dependencies

 * urllib2


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
servers.hostname.resqueweb.failed.total 38667
servers.hostname.resqueweb.pending.current 2
servers.hostname.resqueweb.processed.total 11686516
servers.hostname.resqueweb.queue.low.current 4
servers.hostname.resqueweb.queue.mail.current 3
servers.hostname.resqueweb.queue.normal.current 1
servers.hostname.resqueweb.queue.realtime.current 9
servers.hostname.resqueweb.workers.current 9
servers.hostname.resqueweb.working.current 2
```

