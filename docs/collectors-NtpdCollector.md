NtpdCollector
=====

Collect stats from ntpd

#### Dependencies

    * subprocess


#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>byte_unit</td><td>byte</td><td>Default numeric output(s)</td><td>str</td></tr>
<tr><td>enabled</td><td>False</td><td>Enable collecting these metrics</td><td>bool</td></tr>
<tr><td>measure_collector_time</td><td>False</td><td>Collect the collector run time in ms</td><td>bool</td></tr>
<tr><td>metrics_blacklist</td><td>None</td><td>Regex to match metrics to block. Mutually exclusive with metrics_whitelist</td><td>NoneType</td></tr>
<tr><td>metrics_whitelist</td><td>None</td><td>Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist</td><td>NoneType</td></tr>
<tr><td>ntpdc_bin</td><td>/usr/bin/ntpdc</td><td>Path to ntpdc binary</td><td>str</td></tr>
<tr><td>ntpq_bin</td><td>/usr/bin/ntpq</td><td>Path to ntpq binary</td><td>str</td></tr>
<tr><td>sudo_cmd</td><td>/usr/bin/sudo</td><td>Path to sudo</td><td>str</td></tr>
<tr><td>use_sudo</td><td>False</td><td>Use sudo?</td><td>bool</td></tr>
</table>

#### Example Output

```
servers.hostname.ntpd.delay 0.127
servers.hostname.ntpd.est_error 5.1e-05
servers.hostname.ntpd.frequency -14.24
servers.hostname.ntpd.jitter 0.026
servers.hostname.ntpd.max_error 0.039793
servers.hostname.ntpd.offset -5.427e-06
servers.hostname.ntpd.poll 1024
servers.hostname.ntpd.reach 377
servers.hostname.ntpd.root_dispersion 0.09311
servers.hostname.ntpd.root_distance 0.07663
servers.hostname.ntpd.stratum 2
servers.hostname.ntpd.when 39
```

### This file was generated from the python source
### Please edit the source to make changes

