CephCollector
=====

The CephCollector collects utilization info from the Ceph storage system.

Documentation for ceph perf counters:
http://ceph.com/docs/master/dev/perf_counters/

#### Dependencies

 * ceph [http://ceph.com/]


#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>byte_unit</td><td>byte</td><td>Default numeric output(s)</td><td>str</td></tr>
<tr><td>ceph_binary</td><td>/usr/bin/ceph</td><td>Path to "ceph" executable. Defaults to /usr/bin/ceph.</td><td>str</td></tr>
<tr><td>enabled</td><td>False</td><td>Enable collecting these metrics</td><td>bool</td></tr>
<tr><td>measure_collector_time</td><td>False</td><td>Collect the collector run time in ms</td><td>bool</td></tr>
<tr><td>metrics_blacklist</td><td>None</td><td>Regex to match metrics to block. Mutually exclusive with metrics_whitelist</td><td>NoneType</td></tr>
<tr><td>metrics_whitelist</td><td>None</td><td>Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist</td><td>NoneType</td></tr>
<tr><td>socket_ext</td><td>asok</td><td>Extension for socket filenames. Defaults to "asok"</td><td>str</td></tr>
<tr><td>socket_path</td><td>/var/run/ceph</td><td>The location of the ceph monitoring sockets. Defaults to "/var/run/ceph"</td><td>str</td></tr>
<tr><td>socket_prefix</td><td>ceph-</td><td>The first part of all socket names. Defaults to "ceph-"</td><td>str</td></tr>
</table>

#### Example Output

```
__EXAMPLESHERE__
```

### This file was generated from the python source
### Please edit the source to make changes

