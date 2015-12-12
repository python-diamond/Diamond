DiskUsageCollector
=====

Collect IO Stats

Note: You may need to artificially generate some IO load on a disk/partition
before graphite will generate the metrics.

 * http://www.kernel.org/doc/Documentation/iostats.txt

#### Dependencies

 * /proc/diskstats


#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>byte_unit</td><td>byte</td><td>Default numeric output(s)</td><td>str</td></tr>
<tr><td>devices</td><td>PhysicalDrive[0-9]+$|md[0-9]+$|sd[a-z]+[0-9]*$|x?vd[a-z]+[0-9]*$|disk[0-9]+$|dm\-[0-9]+$</td><td>A regex of which devices to gather metrics for. Defaults to md, sd, xvd, disk, and dm devices</td><td>str</td></tr>
<tr><td>enabled</td><td>False</td><td>Enable collecting these metrics</td><td>bool</td></tr>
<tr><td>measure_collector_time</td><td>False</td><td>Collect the collector run time in ms</td><td>bool</td></tr>
<tr><td>metrics_blacklist</td><td>None</td><td>Regex to match metrics to block. Mutually exclusive with metrics_whitelist</td><td>NoneType</td></tr>
<tr><td>metrics_whitelist</td><td>None</td><td>Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist</td><td>NoneType</td></tr>
<tr><td>sector_size</td><td>512</td><td>The size to use to calculate sector usage</td><td>int</td></tr>
<tr><td>send_zero</td><td>False</td><td>Send io data even when there is no io</td><td>bool</td></tr>
</table>

#### Example Output

```
__EXAMPLESHERE__
```

### This file was generated from the python source
### Please edit the source to make changes

