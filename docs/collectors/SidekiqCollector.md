<!--This file was generated from the python source
Please edit the source to make changes
-->
SidekiqCollector
=====

Collects sidekiq data from Redis

#### Dependencies

 * redis


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
cluster_prefix | None | Redis cluster name prefix | NoneType
databases | 16 | how many database instances to collect | int
enabled | False | Enable collecting these metrics | bool
host | localhost | Redis hostname | str
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
password | None | Redis Auth password | NoneType
ports | 6379 | Redis ports | str
sentinel_name | None | Redis sentinel name | NoneType
sentinel_ports | None | Redis sentinel ports | NoneType

#### Example Output

```
servers.hostname.sidekiq.queue.test-sidekiq.6379.0.queue_1 123
servers.hostname.sidekiq.queue.test-sidekiq.6379.0.retry 100
servers.hostname.sidekiq.queue.test-sidekiq.6379.0.schedule 100
```

