SoftInterruptCollector
=====

The SoftInterruptCollector collects metrics on software interrupts from
/proc/stat

#### Dependencies

 * /proc/stat


#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>byte_unit</td><td>byte</td><td>Default numeric output(s)</td><td>str</td></tr>
<tr><td>enabled</td><td>False</td><td>Enable collecting these metrics</td><td>bool</td></tr>
<tr><td>measure_collector_time</td><td>False</td><td>Collect the collector run time in ms</td><td>bool</td></tr>
<tr><td>metrics_blacklist</td><td>None</td><td>Regex to match metrics to block. Mutually exclusive with metrics_whitelist</td><td>NoneType</td></tr>
<tr><td>metrics_whitelist</td><td>None</td><td>Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist</td><td>NoneType</td></tr>
</table>

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

### This file was generated from the python source
### Please edit the source to make changes

