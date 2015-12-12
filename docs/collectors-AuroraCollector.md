AuroraCollector
=====
None
#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>byte_unit</td><td>byte</td><td>Default numeric output(s)</td><td>str</td></tr>
<tr><td>enabled</td><td>False</td><td>Enable collecting these metrics</td><td>bool</td></tr>
<tr><td>host</td><td>localhost</td><td>Scheduler Hostname</td><td>str</td></tr>
<tr><td>measure_collector_time</td><td>False</td><td>Collect the collector run time in ms</td><td>bool</td></tr>
<tr><td>metrics_blacklist</td><td>None</td><td>Regex to match metrics to block. Mutually exclusive with metrics_whitelist</td><td>NoneType</td></tr>
<tr><td>metrics_whitelist</td><td>None</td><td>Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist</td><td>NoneType</td></tr>
<tr><td>path</td><td>aurora</td><td>Collector path. Defaults to "aurora"</td><td>str</td></tr>
<tr><td>port</td><td>8081</td><td>Scheduler HTTP Metrics Port</td><td>int</td></tr>
<tr><td>scheme</td><td>http</td><td>http</td><td>str</td></tr>
</table>

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

### This file was generated from the python source
### Please edit the source to make changes

