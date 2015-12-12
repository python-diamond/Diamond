LibvirtKVMCollector
=====

Uses libvirt to harvest per KVM instance stats

#### Dependencies

 * python-libvirt, xml


#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>byte_unit</td><td>byte</td><td>Default numeric output(s)</td><td>str</td></tr>
<tr><td>cpu_absolute</td><td>False</td><td>CPU stats reported as percentage by default, or<br>
as cummulative nanoseconds since VM creation if this is True.</td><td>bool</td></tr>
<tr><td>enabled</td><td>False</td><td>Enable collecting these metrics</td><td>bool</td></tr>
<tr><td>measure_collector_time</td><td>False</td><td>Collect the collector run time in ms</td><td>bool</td></tr>
<tr><td>metrics_blacklist</td><td>None</td><td>Regex to match metrics to block. Mutually exclusive with metrics_whitelist</td><td>NoneType</td></tr>
<tr><td>metrics_whitelist</td><td>None</td><td>Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist</td><td>NoneType</td></tr>
<tr><td>sort_by_uuid</td><td>False</td><td>Use the <uuid> of the instance instead of the<br>
 default <name>, useful in Openstack deploments where <name> is only<br>
specific to the compute node</td><td>bool</td></tr>
<tr><td>uri</td><td>qemu:///system</td><td>The libvirt connection URI. By default it's<br>
'qemu:///system'. One decent option is<br>
'qemu+unix:///system?socket=/var/run/libvirt/libvit-sock-ro'.</td><td>str</td></tr>
</table>

#### Example Output

```
__EXAMPLESHERE__
```

### This file was generated from the python source
### Please edit the source to make changes

