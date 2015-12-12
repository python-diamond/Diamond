ConnTrackCollector
=====

Collecting connections tracking statistics from nf_conntrack/ip_conntrack
kernel module.

#### Dependencies

 * nf_conntrack/ip_conntrack kernel module


#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>byte_unit</td><td>byte</td><td>Default numeric output(s)</td><td>str</td></tr>
<tr><td>dir</td><td>/proc/sys/net/ipv4/netfilter,/proc/sys/net/netfilter</td><td>Directories with files of interest, comma seperated</td><td>str</td></tr>
<tr><td>enabled</td><td>False</td><td>Enable collecting these metrics</td><td>bool</td></tr>
<tr><td>files</td><td>ip_conntrack_count,ip_conntrack_max,nf_conntrack_count,nf_conntrack_max</td><td>List of files to collect statistics from</td><td>str</td></tr>
<tr><td>measure_collector_time</td><td>False</td><td>Collect the collector run time in ms</td><td>bool</td></tr>
<tr><td>metrics_blacklist</td><td>None</td><td>Regex to match metrics to block. Mutually exclusive with metrics_whitelist</td><td>NoneType</td></tr>
<tr><td>metrics_whitelist</td><td>None</td><td>Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist</td><td>NoneType</td></tr>
</table>

#### Example Output

```
__EXAMPLESHERE__
```

### This file was generated from the python source
### Please edit the source to make changes

