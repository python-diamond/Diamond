LoadAverageCollector
=====

Uses /proc/loadavg to collect data on load average

#### Dependencies

 * /proc/loadavg


#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>byte_unit</td><td>byte</td><td>Default numeric output(s)</td><td>str</td></tr>
<tr><td>enabled</td><td>False</td><td>Enable collecting these metrics</td><td>bool</td></tr>
<tr><td>measure_collector_time</td><td>False</td><td>Collect the collector run time in ms</td><td>bool</td></tr>
<tr><td>metrics_blacklist</td><td>None</td><td>Regex to match metrics to block. Mutually exclusive with metrics_whitelist</td><td>NoneType</td></tr>
<tr><td>metrics_whitelist</td><td>None</td><td>Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist</td><td>NoneType</td></tr>
<tr><td>simple</td><td>False</td><td>Only collect the 1 minute load average</td><td>str</td></tr>
</table>

#### Example Output

```
servers.hostname.loadavg.01 (0.12, 2)
servers.hostname.loadavg.05 (0.23, 2)
servers.hostname.loadavg.15 (0.34, 2)
servers.hostname.loadavg.processes_running 1
servers.hostname.loadavg.processes_total 235
```

### This file was generated from the python source
### Please edit the source to make changes

