IODriveSNMPCollector
=====

SNMPCollector for Fusion IO DRives Metrics. ( Subclass of snmpCollector )
Based heavily on the NetscalerSNMPCollector.

This collector currently assumes a single IODrive I or IODrive II and not the
DUO, Octals, or multiple IODrive I or IIs. It needs to be enhanced to account
for multiple fio devices. ( Donations being accepted )

The metric path is configured to be under servers.<host>.<device> where host
and device is defined in the IODriveSNMPCollector.conf.  So given the example
conf below the metricpath would be
"servers.my_host.iodrive.<metric> name.

# EXAMPLE CONF file

enabled = True
[devices]
[[iodrive]]
host = my_host
port = 161
community = mycommunitystring


#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>byte_unit</td><td>byte</td><td>Default numeric output(s)</td><td>str</td></tr>
<tr><td>community</td><td></td><td>SNMP community</td><td></td></tr>
<tr><td>enabled</td><td>False</td><td>Enable collecting these metrics</td><td>bool</td></tr>
<tr><td>host</td><td></td><td>Host address</td><td></td></tr>
<tr><td>measure_collector_time</td><td>False</td><td>Collect the collector run time in ms</td><td>bool</td></tr>
<tr><td>metrics_blacklist</td><td>None</td><td>Regex to match metrics to block. Mutually exclusive with metrics_whitelist</td><td>NoneType</td></tr>
<tr><td>metrics_whitelist</td><td>None</td><td>Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist</td><td>NoneType</td></tr>
<tr><td>port</td><td></td><td>SNMP port to collect snmp data</td><td></td></tr>
<tr><td>retries</td><td>3</td><td>Number of times to retry before bailing</td><td>int</td></tr>
<tr><td>timeout</td><td>15</td><td>Seconds before timing out the snmp connection</td><td>int</td></tr>
</table>

#### Example Output

```
__EXAMPLESHERE__
```

### This file was generated from the python source
### Please edit the source to make changes

