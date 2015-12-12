BindCollector
=====

Collects stats from bind 9.5's statistics server

#### Dependencies

 * [bind 9.5](http://www.isc.org/software/bind/new-features/9.5)
    configured with libxml2 and statistics-channels


#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>byte_unit</td><td>byte</td><td>Default numeric output(s)</td><td>str</td></tr>
<tr><td>enabled</td><td>False</td><td>Enable collecting these metrics</td><td>bool</td></tr>
<tr><td>host</td><td>localhost</td><td></td><td>str</td></tr>
<tr><td>measure_collector_time</td><td>False</td><td>Collect the collector run time in ms</td><td>bool</td></tr>
<tr><td>metrics_blacklist</td><td>None</td><td>Regex to match metrics to block. Mutually exclusive with metrics_whitelist</td><td>NoneType</td></tr>
<tr><td>metrics_whitelist</td><td>None</td><td>Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist</td><td>NoneType</td></tr>
<tr><td>port</td><td>8080</td><td></td><td>int</td></tr>
<tr><td>publish</td><td>resolver, server, zonemgmt, sockets, memory,</td><td>Available stats:<br>
 - resolver (Per-view resolver and cache statistics)<br>
 - server (Incoming requests and their answers)<br>
 - zonemgmt (Zone management requests/responses)<br>
 - sockets (Socket statistics)<br>
 - memory (Global memory usage)<br>
</td><td>list</td></tr>
<tr><td>publish_view_bind</td><td>False</td><td></td><td>bool</td></tr>
<tr><td>publish_view_meta</td><td>False</td><td></td><td>bool</td></tr>
</table>

#### Example Output

```
__EXAMPLESHERE__
```

### This file was generated from the python source
### Please edit the source to make changes

