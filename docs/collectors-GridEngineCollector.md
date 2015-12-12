GridEngineCollector
=====

The GridEngineCollector parses qstat statistics from Sun Grid Engine,
Univa Grid Engine and Open Grid Scheduler.

#### Dependencies

 * Grid Engine qstat


#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>bin_path</td><td>/opt/gridengine/bin/lx-amd64/qstat</td><td>The path to Grid Engine's qstat</td><td>str</td></tr>
<tr><td>byte_unit</td><td>byte</td><td>Default numeric output(s)</td><td>str</td></tr>
<tr><td>enabled</td><td>False</td><td>Enable collecting these metrics</td><td>bool</td></tr>
<tr><td>measure_collector_time</td><td>False</td><td>Collect the collector run time in ms</td><td>bool</td></tr>
<tr><td>metrics_blacklist</td><td>None</td><td>Regex to match metrics to block. Mutually exclusive with metrics_whitelist</td><td>NoneType</td></tr>
<tr><td>metrics_whitelist</td><td>None</td><td>Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist</td><td>NoneType</td></tr>
<tr><td>sge_root</td><td>/opt/gridengine</td><td>The SGE_ROOT value to provide to qstat</td><td>str</td></tr>
</table>

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

### This file was generated from the python source
### Please edit the source to make changes

