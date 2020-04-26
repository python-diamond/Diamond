<!--This file was generated from the python source
Please edit the source to make changes
-->
AuroraCollector
=====
None
#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
host | localhost | Scheduler Hostname | str
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
path | aurora | Collector path. Defaults to "aurora" | str
port | 8081 | Scheduler HTTP Metrics Port | int
scheme | http | http | str

#### Example Output

```
servers.hostname.aurora.async.tasks.completed 11117.0
servers.hostname.aurora.attribute.store.fetch.all.events 24.0
servers.hostname.aurora.attribute.store.fetch.all.events.per.sec 0.0
servers.hostname.aurora.attribute.store.fetch.all.nanos.per.event 0.0
servers.hostname.aurora.attribute.store.fetch.all.nanos.total 90208119.0
servers.hostname.aurora.attribute.store.fetch.all.nanos.total.per.sec 0.0
servers.hostname.aurora.attribute.store.fetch.one.events 33024.0
servers.hostname.aurora.tasks.FAILED.computers.prod.computer-traffic-analysis 517.0
servers.hostname.aurora.tasks.FAILED.reporting.prod.report-processing 2.0
```

