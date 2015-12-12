ResqueWebCollector
=====

Collects data for Resque Web

#### Dependencies

 * urllib2


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

### This file was generated from the python source
### Please edit the source to make changes

