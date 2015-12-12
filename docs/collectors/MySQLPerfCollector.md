MySQLPerfCollector
=====


Diamond collector that monitors relevant MySQL performance_schema values
For now only monitors replication load

[Blog](http://bit.ly/PbSkbN) announcement.

[Snippet](http://bit.ly/SHwYhT) to build example graph.

#### Dependencies

 * MySQLdb
 * MySQL 5.5.3+


#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>byte_unit</td><td>byte</td><td>Default numeric output(s)</td><td>str</td></tr>
<tr><td>enabled</td><td>False</td><td>Enable collecting these metrics</td><td>bool</td></tr>
<tr><td>hosts</td><td>,</td><td>List of hosts to collect from. Format is yourusername:yourpassword@host:port/performance_schema[/nickname]</td><td>list</td></tr>
<tr><td>measure_collector_time</td><td>False</td><td>Collect the collector run time in ms</td><td>bool</td></tr>
<tr><td>metrics_blacklist</td><td>None</td><td>Regex to match metrics to block. Mutually exclusive with metrics_whitelist</td><td>NoneType</td></tr>
<tr><td>metrics_whitelist</td><td>None</td><td>Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist</td><td>NoneType</td></tr>
<tr><td>slave</td><td>False</td><td>Collect Slave Replication Metrics</td><td>str</td></tr>
</table>

#### Example Output

```
__EXAMPLESHERE__
```

### This file was generated from the python source
### Please edit the source to make changes

