MountStatsCollector
=====

The function of MountStatsCollector is to parse the detailed per-mount NFS
performance statistics provided by `/proc/self/mountstats` (reads, writes,
remote procedure call count/latency, etc.) and provide counters to Diamond.
Filesystems may be included/excluded using a regular expression filter,
like the existing disk check collectors.

#### Dependencies

 * /proc/self/mountstats


#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>byte_unit</td><td>byte</td><td>Default numeric output(s)</td><td>str</td></tr>
<tr><td>enabled</td><td>False</td><td>Enable collecting these metrics</td><td>bool</td></tr>
<tr><td>exclude_filters</td><td>,</td><td>A list of regex patterns. Any filesystem matching any of these patterns will be excluded from mount stats metrics collection.</td><td>list</td></tr>
<tr><td>include_filters</td><td>,</td><td>A list of regex patterns. Any filesystem matching any of these patterns will be included from mount stats metrics collection.</td><td>list</td></tr>
<tr><td>measure_collector_time</td><td>False</td><td>Collect the collector run time in ms</td><td>bool</td></tr>
<tr><td>metrics_blacklist</td><td>None</td><td>Regex to match metrics to block. Mutually exclusive with metrics_whitelist</td><td>NoneType</td></tr>
<tr><td>metrics_whitelist</td><td>None</td><td>Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist</td><td>NoneType</td></tr>
<tr><td>sudo_cmd</td><td>/usr/bin/sudo</td><td>Path to sudo</td><td>str</td></tr>
<tr><td>use_sudo</td><td>False</td><td>Use sudo?</td><td>bool</td></tr>
</table>

#### Example Output

```
__EXAMPLESHERE__
```

### This file was generated from the python source
### Please edit the source to make changes

