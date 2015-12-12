AmavisCollector
=====

Collector that reports amavis metrics as reported by amavisd-agent

#### Dependencies

* amavisd-agent must be present in PATH


#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>amavisd_exe</td><td>/usr/sbin/amavisd-agent</td><td>The path to amavisd-agent</td><td>str</td></tr>
<tr><td>byte_unit</td><td>byte</td><td>Default numeric output(s)</td><td>str</td></tr>
<tr><td>enabled</td><td>False</td><td>Enable collecting these metrics</td><td>bool</td></tr>
<tr><td>measure_collector_time</td><td>False</td><td>Collect the collector run time in ms</td><td>bool</td></tr>
<tr><td>metrics_blacklist</td><td>None</td><td>Regex to match metrics to block. Mutually exclusive with metrics_whitelist</td><td>NoneType</td></tr>
<tr><td>metrics_whitelist</td><td>None</td><td>Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist</td><td>NoneType</td></tr>
<tr><td>sudo_exe</td><td>/usr/bin/sudo</td><td>The path to sudo</td><td>str</td></tr>
<tr><td>sudo_user</td><td>amavis</td><td>The user to use if using sudo</td><td>str</td></tr>
<tr><td>use_sudo</td><td>False</td><td>Call amavisd-agent using sudo</td><td>bool</td></tr>
</table>

#### Example Output

```
servers.hostname.amavis.OutMsgsProtoSMTPRelay.count 22778
servers.hostname.amavis.OutMsgsProtoSMTPRelay.frequency 41
servers.hostname.amavis.OutMsgsProtoSMTPRelay.percentage 71.5
servers.hostname.amavis.OutMsgsSizeProtoSMTP.frequency 0
servers.hostname.amavis.OutMsgsSizeProtoSMTP.percentage 96.4
servers.hostname.amavis.OutMsgsSizeProtoSMTP.size 116
servers.hostname.amavis.TimeElapsedDecoding.frequency 0.024
servers.hostname.amavis.TimeElapsedDecoding.time 652
servers.hostname.amavis.sysUpTime.time 198103058
servers.hostname.amavis.virus.byname.Eicar-Test-Signature.count 4436
servers.hostname.amavis.virus.byname.Eicar-Test-Signature.frequency 8
servers.hostname.amavis.virus.byname.Eicar-Test-Signature.percentage 100.0
```

### This file was generated from the python source
### Please edit the source to make changes

