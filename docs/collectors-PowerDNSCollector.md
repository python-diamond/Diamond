PowerDNSCollector
=====

Collects all metrics exported by the powerdns nameserver using the
pdns_control binary.

#### Dependencies

 * pdns_control


#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>bin</td><td>/usr/bin/pdns_control</td><td>The path to the pdns_control binary</td><td>str</td></tr>
<tr><td>byte_unit</td><td>byte</td><td>Default numeric output(s)</td><td>str</td></tr>
<tr><td>enabled</td><td>False</td><td>Enable collecting these metrics</td><td>bool</td></tr>
<tr><td>measure_collector_time</td><td>False</td><td>Collect the collector run time in ms</td><td>bool</td></tr>
<tr><td>metrics_blacklist</td><td>None</td><td>Regex to match metrics to block. Mutually exclusive with metrics_whitelist</td><td>NoneType</td></tr>
<tr><td>metrics_whitelist</td><td>None</td><td>Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist</td><td>NoneType</td></tr>
<tr><td>sudo_cmd</td><td>/usr/bin/sudo</td><td>Path to sudo</td><td>str</td></tr>
<tr><td>use_sudo</td><td>False</td><td>Use sudo?</td><td>bool</td></tr>
</table>

#### Example Output

```
servers.hostname.powerdns.corrupt-packets 1.0
servers.hostname.powerdns.deferred-cache-inserts 2.0
servers.hostname.powerdns.deferred-cache-lookup 3.0
servers.hostname.powerdns.latency 4.0
servers.hostname.powerdns.packetcache-hit 5.0
servers.hostname.powerdns.packetcache-miss 6.0
servers.hostname.powerdns.packetcache-size 7.0
servers.hostname.powerdns.qsize-q 8.0
servers.hostname.powerdns.query-cache-hit 9.0
servers.hostname.powerdns.query-cache-miss 10.0
servers.hostname.powerdns.recursing-answers 11.0
servers.hostname.powerdns.recursing-questions 12.0
servers.hostname.powerdns.servfail-packets 13.0
servers.hostname.powerdns.tcp-answers 14.0
servers.hostname.powerdns.tcp-queries 15.0
servers.hostname.powerdns.timedout-packets 16.0
servers.hostname.powerdns.udp-answers 17.0
servers.hostname.powerdns.udp-queries 18.0
servers.hostname.powerdns.udp4-answers 19.0
servers.hostname.powerdns.udp4-queries 20.0
servers.hostname.powerdns.udp6-answers 21.0
servers.hostname.powerdns.udp6-queries 22.0
```

### This file was generated from the python source
### Please edit the source to make changes

