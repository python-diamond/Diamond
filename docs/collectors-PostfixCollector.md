PostfixCollector
=====

Collect stats from postfix-stats. postfix-stats is a simple threaded stats
aggregator for Postfix. When running as a syslog destination, it can be used to
get realtime cumulative stats.

#### Dependencies

 * socket
 * json (or simplejson)
 * [postfix-stats](https://github.com/disqus/postfix-stats)


#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>byte_unit</td><td>byte</td><td>Default numeric output(s)</td><td>str</td></tr>
<tr><td>enabled</td><td>False</td><td>Enable collecting these metrics</td><td>bool</td></tr>
<tr><td>host</td><td>localhost</td><td>Hostname to connect to</td><td>str</td></tr>
<tr><td>include_clients</td><td>True</td><td>Include client connection stats</td><td>bool</td></tr>
<tr><td>measure_collector_time</td><td>False</td><td>Collect the collector run time in ms</td><td>bool</td></tr>
<tr><td>metrics_blacklist</td><td>None</td><td>Regex to match metrics to block. Mutually exclusive with metrics_whitelist</td><td>NoneType</td></tr>
<tr><td>metrics_whitelist</td><td>None</td><td>Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist</td><td>NoneType</td></tr>
<tr><td>port</td><td>7777</td><td>Port to connect to</td><td>int</td></tr>
</table>

#### Example Output

```
servers.hostname.postfix.clients.127_0_0_1 1
servers.hostname.postfix.send.resp_codes.2_0_0 5
servers.hostname.postfix.send.status.sent 4
```

### This file was generated from the python source
### Please edit the source to make changes

