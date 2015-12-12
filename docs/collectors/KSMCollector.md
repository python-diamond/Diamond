KSMCollector
=====

This class collects 'Kernel Samepage Merging' statistics.
KSM is a memory de-duplication feature of the Linux Kernel (2.6.32+).

It can be enabled, if compiled into your kernel, by echoing 1 to
/sys/kernel/mm/ksm/run. You can find more information about KSM at
[http://www.linux-kvm.org/page/KSM](http://www.linux-kvm.org/page/KSM).

#### Dependencies

 * KSM built into your kernel. It does not have to be enabled, but the stats
 will be less than useful if it isn't:-)


#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>byte_unit</td><td>byte</td><td>Default numeric output(s)</td><td>str</td></tr>
<tr><td>enabled</td><td>False</td><td>Enable collecting these metrics</td><td>bool</td></tr>
<tr><td>ksm_path</td><td>/sys/kernel/mm/ksm</td><td>location where KSM kernel data can be found</td><td>str</td></tr>
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

