IPCollector
=====

The IPCollector class collects metrics on IP stats

#### Dependencies

 * /proc/net/snmp

#### Allowed Metric Names
<table>
<tr><th>Name</th></tr>
<tr><th>InAddrErrors</th></tr>
<tr><th>InDelivers</th></tr>
<tr><th>InDiscards</th></tr>
<tr><th>InHdrErrors</th></tr>
<tr><th>InReceives</th></tr>
<tr><th>InUnknownProtos</th></tr>
<tr><th>OutDiscards</th></tr>
<tr><th>OutNoRoutes</th></tr>
<tr><th>OutRequests</th></tr>
</table>


#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>allowed_names</td><td>InAddrErrors, InDelivers, InDiscards, InHdrErrors, InReceives, InUnknownProtos, OutDiscards, OutNoRoutes, OutRequests</td><td>list of entries to collect, empty to collect all</td><td>str</td></tr>
<tr><td>byte_unit</td><td>byte</td><td>Default numeric output(s)</td><td>str</td></tr>
<tr><td>enabled</td><td>False</td><td>Enable collecting these metrics</td><td>bool</td></tr>
<tr><td>measure_collector_time</td><td>False</td><td>Collect the collector run time in ms</td><td>bool</td></tr>
<tr><td>metrics_blacklist</td><td>None</td><td>Regex to match metrics to block. Mutually exclusive with metrics_whitelist</td><td>NoneType</td></tr>
<tr><td>metrics_whitelist</td><td>None</td><td>Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist</td><td>NoneType</td></tr>
</table>

#### Example Output

```
__EXAMPLESHERE__
```

### This file was generated from the python source
### Please edit the source to make changes

