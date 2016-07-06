<!--This file was generated from the python source
Please edit the source to make changes
-->
AerospikeCollector
=====

Collect statistics from Aerospike

#### Dependencies

 * socket
 * telnetlib
 * re



#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
latency | True | Collect latency metrics | bool
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
namespace_statistics_whitelist | objects, evicted-objects, expired-objects, used-bytes-memory, data-used-bytes-memory, index-used-bytes-memory, used-bytes-disk, memory-size, total-bytes-memory, total-bytes-disk, migrate-tx-partitions-initial, migrate-tx-partitions-remaining, migrate-rx-partitions-initial, migrate-rx-partitions-remaining, | List of per-namespace statistics values to collect | list
namespaces | True | Collect per-namespace metrics | bool
namespaces_whitelist | False | List of namespaces to collect metrics from (default is to collect from all) | bool
path | aerospike | Metric path | str
req_host | localhost | Hostname | str
req_port | 3003 | Port | int
statistics | True | Collect statistics | bool
statistics_whitelist | total-bytes-memory, total-bytes-disk, used-bytes-memory, used-bytes-disk, free-pct-memory, free-pct-disk, data-used-bytes-memory, cluster_size, objects, client_connections, index-used-bytes-memory, | List of global statistics values to collect | list
throughput | True | Collect throughput metrics | bool

#### Example Output

```
__EXAMPLESHERE__
```

