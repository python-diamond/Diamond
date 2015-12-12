ChronydCollector
=====

Collect metrics from chrony - http://chrony.tuxfamily.org/

#### Dependencies

 * subprocess


#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>bin</td><td>/usr/bin/chronyc</td><td>The path to the chronyc binary</td><td>str</td></tr>
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
servers.hostname.chrony.178_251_120_16.offset_ms -7e-05
servers.hostname.chrony.85_12_29_43.offset_ms -0.785
servers.hostname.chrony.85_234_197_3.offset_ms 0.08
servers.hostname.chrony.85_255_214_66.offset_ms 0.386
```

### This file was generated from the python source
### Please edit the source to make changes

