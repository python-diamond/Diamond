<!--This file was generated from the python source
Please edit the source to make changes
-->
GridEngineCollector
=====

The GridEngineCollector parses qstat statistics from Sun Grid Engine,
Univa Grid Engine and Open Grid Scheduler.

#### Dependencies

 * Grid Engine qstat


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
bin_path | /opt/gridengine/bin/lx-amd64/qstat | The path to Grid Engine's qstat | str
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
sge_root | /opt/gridengine | The SGE_ROOT value to provide to qstat | str

#### Example Output

```
servers.hostname.gridengine.queues.hadoop.available 0
servers.hostname.gridengine.queues.hadoop.load 0.00532
servers.hostname.gridengine.queues.hadoop.manual_intervention 36
servers.hostname.gridengine.queues.hadoop.resv 0
servers.hostname.gridengine.queues.hadoop.temp_disabled 0
servers.hostname.gridengine.queues.hadoop.total 36
servers.hostname.gridengine.queues.hadoop.used 0
servers.hostname.gridengine.queues.primary_q.available 1152
servers.hostname.gridengine.queues.primary_q.load 0.20509
servers.hostname.gridengine.queues.primary_q.manual_intervention 0
servers.hostname.gridengine.queues.primary_q.resv 0
servers.hostname.gridengine.queues.primary_q.temp_disabled 0
servers.hostname.gridengine.queues.primary_q.total 2176
servers.hostname.gridengine.queues.primary_q.used 1024
servers.hostname.gridengine.queues.secondary_q.available 1007
servers.hostname.gridengine.queues.secondary_q.load 0.0046
servers.hostname.gridengine.queues.secondary_q.manual_intervention 0
servers.hostname.gridengine.queues.secondary_q.resv 0
servers.hostname.gridengine.queues.secondary_q.temp_disabled 1
servers.hostname.gridengine.queues.secondary_q.total 1121
servers.hostname.gridengine.queues.secondary_q.used 145
```

