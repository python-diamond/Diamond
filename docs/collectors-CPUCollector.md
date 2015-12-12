CPUCollector
=====

The CPUCollector collects CPU utilization metric using /proc/stat.

#### Dependencies

 * /proc/stat


#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>byte_unit</td><td>byte</td><td>Default numeric output(s)</td><td>str</td></tr>
<tr><td>enabled</td><td>False</td><td>Enable collecting these metrics</td><td>bool</td></tr>
<tr><td>measure_collector_time</td><td>False</td><td>Collect the collector run time in ms</td><td>bool</td></tr>
<tr><td>metrics_blacklist</td><td>None</td><td>Regex to match metrics to block. Mutually exclusive with metrics_whitelist</td><td>NoneType</td></tr>
<tr><td>metrics_whitelist</td><td>None</td><td>Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist</td><td>NoneType</td></tr>
<tr><td>normalize</td><td>False</td><td>for cpu totals, divide by the number of CPUs</td><td>str</td></tr>
<tr><td>percore</td><td>True</td><td>Collect metrics per cpu core or just total</td><td>str</td></tr>
<tr><td>simple</td><td>False</td><td>only return aggregate CPU% metric</td><td>str</td></tr>
</table>

#### Example Output

```
servers.hostname.cpu.total.idle 2440.8
servers.hostname.cpu.total.iowait 0.2
servers.hostname.cpu.total.nice 0.0
servers.hostname.cpu.total.system 0.2
servers.hostname.cpu.total.user 0.4
```

### This file was generated from the python source
### Please edit the source to make changes

