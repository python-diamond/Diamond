IPMISensorCollector
=====

This collector uses the [ipmitool](http://openipmi.sourceforge.net/) to read
hardware sensors from servers
using the Intelligent Platform Management Interface (IPMI). IPMI is very common
with server hardware but usually not available in consumer hardware.

#### Dependencies

 * [ipmitool](http://openipmi.sourceforge.net/)


#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>bin</td><td>/usr/bin/ipmitool</td><td>Path to the ipmitool binary</td><td>str</td></tr>
<tr><td>byte_unit</td><td>byte</td><td>Default numeric output(s)</td><td>str</td></tr>
<tr><td>delimiter</td><td>.</td><td>Parse blanks in sensor names into a delimiter</td><td>str</td></tr>
<tr><td>enabled</td><td>False</td><td>Enable collecting these metrics</td><td>bool</td></tr>
<tr><td>measure_collector_time</td><td>False</td><td>Collect the collector run time in ms</td><td>bool</td></tr>
<tr><td>metrics_blacklist</td><td>None</td><td>Regex to match metrics to block. Mutually exclusive with metrics_whitelist</td><td>NoneType</td></tr>
<tr><td>metrics_whitelist</td><td>None</td><td>Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist</td><td>NoneType</td></tr>
<tr><td>sudo_cmd</td><td>/usr/bin/sudo</td><td>Path to sudo</td><td>str</td></tr>
<tr><td>thresholds</td><td>False</td><td>Collect thresholds as well as reading</td><td>bool</td></tr>
<tr><td>use_sudo</td><td>False</td><td>Use sudo?</td><td>bool</td></tr>
</table>

#### Example Output

```
servers.hostname.ipmi.sensors.+12V 12.031
servers.hostname.ipmi.sensors.+1_1V 1.112
servers.hostname.ipmi.sensors.+1_5V 1.512
servers.hostname.ipmi.sensors.+1_8V 1.824
servers.hostname.ipmi.sensors.+3_3V 3.288
servers.hostname.ipmi.sensors.+3_3VSB 3.24
servers.hostname.ipmi.sensors.+5V 4.992
servers.hostname.ipmi.sensors.CPU1.DIMM 1.512
servers.hostname.ipmi.sensors.CPU1.Temp 0.0
servers.hostname.ipmi.sensors.CPU1.VTT 1.12
servers.hostname.ipmi.sensors.CPU1.Vcore 1.08
servers.hostname.ipmi.sensors.CPU2.DIMM 1.512
servers.hostname.ipmi.sensors.CPU2.Temp 0.0
servers.hostname.ipmi.sensors.CPU2.VTT 1.176
servers.hostname.ipmi.sensors.CPU2.Vcore 1.0
servers.hostname.ipmi.sensors.Fan1 4185.0
servers.hostname.ipmi.sensors.Fan2 4185.0
servers.hostname.ipmi.sensors.Fan3 4185.0
servers.hostname.ipmi.sensors.Fan7 3915.0
servers.hostname.ipmi.sensors.Fan8 3915.0
servers.hostname.ipmi.sensors.Intrusion 0.0
servers.hostname.ipmi.sensors.P1-DIMM1A.Temp 41.0
servers.hostname.ipmi.sensors.P1-DIMM1B.Temp 39.0
servers.hostname.ipmi.sensors.P1-DIMM2A.Temp 38.0
servers.hostname.ipmi.sensors.P1-DIMM2B.Temp 40.0
servers.hostname.ipmi.sensors.P1-DIMM3A.Temp 37.0
servers.hostname.ipmi.sensors.P1-DIMM3B.Temp 38.0
servers.hostname.ipmi.sensors.P2-DIMM1A.Temp 39.0
servers.hostname.ipmi.sensors.P2-DIMM1B.Temp 38.0
servers.hostname.ipmi.sensors.P2-DIMM2A.Temp 39.0
servers.hostname.ipmi.sensors.P2-DIMM2B.Temp 39.0
servers.hostname.ipmi.sensors.P2-DIMM3A.Temp 39.0
servers.hostname.ipmi.sensors.P2-DIMM3B.Temp 40.0
servers.hostname.ipmi.sensors.PS.Status 0.0
servers.hostname.ipmi.sensors.System.Temp 32.0
servers.hostname.ipmi.sensors.VBAT 3.24
```

### This file was generated from the python source
### Please edit the source to make changes

