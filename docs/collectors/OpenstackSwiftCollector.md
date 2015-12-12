OpenstackSwiftCollector
=====

Openstack swift collector.

#### Dependencies

 * swift-dispersion-report commandline tool (for dispersion report)
   if using this, make sure swift.conf and dispersion.conf are readable by
   diamond also get an idea of the runtime of a swift-dispersion-report call
   and make sure the collect interval is high enough to avoid contention.
 * swift commandline tool (for container_metrics)

both of these should come installed with swift

#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>account</td><td></td><td>swift auth account (for enable_container_metrics)</td><td></td></tr>
<tr><td>auth_url</td><td></td><td>authentication url (for enable_container_metrics)</td><td></td></tr>
<tr><td>byte_unit</td><td>byte</td><td>Default numeric output(s)</td><td>str</td></tr>
<tr><td>containers</td><td></td><td>containers on which to count number of objects, space separated list (for enable_container_metrics)</td><td></td></tr>
<tr><td>enable_container_metrics</td><td>True</td><td>gather containers metrics (# objects, bytes used, x_timestamp. default True)</td><td>bool</td></tr>
<tr><td>enable_dispersion_report</td><td>False</td><td>gather swift-dispersion-report metrics (default False)</td><td>bool</td></tr>
<tr><td>enabled</td><td>False</td><td>Enable collecting these metrics</td><td>bool</td></tr>
<tr><td>measure_collector_time</td><td>False</td><td>Collect the collector run time in ms</td><td>bool</td></tr>
<tr><td>metrics_blacklist</td><td>None</td><td>Regex to match metrics to block. Mutually exclusive with metrics_whitelist</td><td>NoneType</td></tr>
<tr><td>metrics_whitelist</td><td>None</td><td>Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist</td><td>NoneType</td></tr>
<tr><td>password</td><td></td><td>swift auth password (for enable_container_metrics)</td><td></td></tr>
<tr><td>user</td><td></td><td>swift auth user (for enable_container_metrics)</td><td></td></tr>
</table>

#### Example Output

```
__EXAMPLESHERE__
```

### This file was generated from the python source
### Please edit the source to make changes

