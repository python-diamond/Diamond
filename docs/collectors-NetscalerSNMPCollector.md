NetscalerSNMPCollector
=====

SNMPCollector for Netscaler Metrics

NetScaler is a network appliance manufactured by Citrix providing level 4 load
balancing, firewall, proxy and VPN functions.


#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>byte_unit</td><td>byte</td><td>Default numeric output(s)</td><td>str</td></tr>
<tr><td>community</td><td></td><td>SNMP community</td><td></td></tr>
<tr><td>enabled</td><td>False</td><td>Enable collecting these metrics</td><td>bool</td></tr>
<tr><td>exclude_service_type</td><td>,</td><td>list of service types to exclude (see MIB EntityProtocolType)</td><td>list</td></tr>
<tr><td>exclude_vserver_type</td><td>,</td><td>list of vserver types to exclude (see MIB EntityProtocolType)</td><td>list</td></tr>
<tr><td>host</td><td></td><td>netscaler dns address</td><td></td></tr>
<tr><td>measure_collector_time</td><td>False</td><td>Collect the collector run time in ms</td><td>bool</td></tr>
<tr><td>metrics_blacklist</td><td>None</td><td>Regex to match metrics to block. Mutually exclusive with metrics_whitelist</td><td>NoneType</td></tr>
<tr><td>metrics_whitelist</td><td>None</td><td>Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist</td><td>NoneType</td></tr>
<tr><td>port</td><td></td><td>Netscaler port to collect snmp data</td><td></td></tr>
<tr><td>retries</td><td>3</td><td>Number of times to retry before bailing</td><td>int</td></tr>
<tr><td>timeout</td><td>15</td><td>Seconds before timing out the snmp connection</td><td>int</td></tr>
</table>

#### Example Output

```
__EXAMPLESHERE__
```

### This file was generated from the python source
### Please edit the source to make changes

