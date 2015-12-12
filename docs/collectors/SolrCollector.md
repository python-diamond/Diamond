SolrCollector
=====

Collect the solr stats for the local node

#### Dependencies

 * posixpath
 * urllib2
 * json


#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>byte_unit</td><td>byte</td><td>Default numeric output(s)</td><td>str</td></tr>
<tr><td>core</td><td>None</td><td>Which core info should collect (default: all cores)</td><td>NoneType</td></tr>
<tr><td>enabled</td><td>False</td><td>Enable collecting these metrics</td><td>bool</td></tr>
<tr><td>host</td><td>localhost</td><td></td><td>str</td></tr>
<tr><td>measure_collector_time</td><td>False</td><td>Collect the collector run time in ms</td><td>bool</td></tr>
<tr><td>metrics_blacklist</td><td>None</td><td>Regex to match metrics to block. Mutually exclusive with metrics_whitelist</td><td>NoneType</td></tr>
<tr><td>metrics_whitelist</td><td>None</td><td>Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist</td><td>NoneType</td></tr>
<tr><td>port</td><td>8983</td><td></td><td>int</td></tr>
<tr><td>stats</td><td>jvm, core, response, query, update, cache,</td><td>Available stats: <br>
 - core (Core stats)<br>
 - response (Ping response stats)<br>
 - query (Query Handler stats)<br>
 - update (Update Handler stats)<br>
 - cache (fieldValue, filter, document & queryResult cache stats)<br>
 - jvm (JVM information) <br>
</td><td>list</td></tr>
</table>

#### Example Output

```
__EXAMPLESHERE__
```

### This file was generated from the python source
### Please edit the source to make changes

