ElasticSearchCollector
=====

Collect the elasticsearch stats for the local node.

Supports multiple instances. When using the 'instances'
parameter the instance alias will be appended to the
'path' parameter.

#### Dependencies

 * urlib2


#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>byte_unit</td><td>byte</td><td>Default numeric output(s)</td><td>str</td></tr>
<tr><td>enabled</td><td>False</td><td>Enable collecting these metrics</td><td>bool</td></tr>
<tr><td>host</td><td>127.0.0.1</td><td></td><td>str</td></tr>
<tr><td>instances</td><td>,</td><td>List of instances. When set this overrides the 'host' and 'port' settings. Instance format: instance [<alias>@]<hostname>[:<port>]</td><td>list</td></tr>
<tr><td>logstash_mode</td><td>False</td><td>If 'indices' stats are gathered, remove the YYYY.MM.DD suffix from the index name (e.g. logstash-adm-syslog-2014.01.03) and use that as a bucket for all 'day' index stats.</td><td>bool</td></tr>
<tr><td>measure_collector_time</td><td>False</td><td>Collect the collector run time in ms</td><td>bool</td></tr>
<tr><td>metrics_blacklist</td><td>None</td><td>Regex to match metrics to block. Mutually exclusive with metrics_whitelist</td><td>NoneType</td></tr>
<tr><td>metrics_whitelist</td><td>None</td><td>Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist</td><td>NoneType</td></tr>
<tr><td>port</td><td>9200</td><td></td><td>int</td></tr>
<tr><td>stats</td><td>jvm, thread_pool, indices,</td><td>Available stats:<br>
 - jvm (JVM information)<br>
 - thread_pool (Thread pool information)<br>
 - indices (Individual index stats)<br>
</td><td>list</td></tr>
</table>

#### Example Output

```
__EXAMPLESHERE__
```

### This file was generated from the python source
### Please edit the source to make changes

