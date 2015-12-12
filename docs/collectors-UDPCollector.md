UDPCollector
=====

The UDPCollector class collects metrics on UDP stats (surprise!)

#### Dependencies

 * /proc/net/snmp


#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>allowed_names</td><td>InDatagrams, NoPorts, InErrors, OutDatagrams, RcvbufErrors, SndbufErrors</td><td>list of entries to collect, empty to collect all</td><td>str</td></tr>
<tr><td>byte_unit</td><td>byte</td><td>Default numeric output(s)</td><td>str</td></tr>
<tr><td>enabled</td><td>False</td><td>Enable collecting these metrics</td><td>bool</td></tr>
<tr><td>measure_collector_time</td><td>False</td><td>Collect the collector run time in ms</td><td>bool</td></tr>
<tr><td>metrics_blacklist</td><td>None</td><td>Regex to match metrics to block. Mutually exclusive with metrics_whitelist</td><td>NoneType</td></tr>
<tr><td>metrics_whitelist</td><td>None</td><td>Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist</td><td>NoneType</td></tr>
</table>

#### Example Output

```
servers.hostname.udp.InDatagrams 352320636.0
servers.hostname.udp.InErrors 5.0
servers.hostname.udp.NoPorts 449.0
servers.hostname.udp.OutDatagrams 352353358.0
```

### This file was generated from the python source
### Please edit the source to make changes

