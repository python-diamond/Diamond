MemoryCollector
=====

This class collects data on memory utilization

Note that MemFree may report no memory free. This may not actually be the case,
as memory is allocated to Buffers and Cache as well. See
[this link](http://www.linuxatemyram.com/) for more details.

#### Dependencies

* /proc/meminfo or psutil


#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>byte_unit</td><td>byte</td><td>Default numeric output(s)</td><td>str</td></tr>
<tr><td>detailed</td><td></td><td>Set to True to Collect all the nodes</td><td></td></tr>
<tr><td>enabled</td><td>False</td><td>Enable collecting these metrics</td><td>bool</td></tr>
<tr><td>measure_collector_time</td><td>False</td><td>Collect the collector run time in ms</td><td>bool</td></tr>
<tr><td>metrics_blacklist</td><td>None</td><td>Regex to match metrics to block. Mutually exclusive with metrics_whitelist</td><td>NoneType</td></tr>
<tr><td>metrics_whitelist</td><td>None</td><td>Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist</td><td>NoneType</td></tr>
</table>

#### Example Output

```
servers.hostname.memory.Active 10022168
servers.hostname.memory.Buffers 1526304
servers.hostname.memory.Cached 10726736
servers.hostname.memory.Dirty 24748
servers.hostname.memory.Inactive 2524928
servers.hostname.memory.MemFree 35194496
servers.hostname.memory.MemTotal 49554212
servers.hostname.memory.Shmem 276
servers.hostname.memory.SwapCached 0
servers.hostname.memory.SwapFree 262143996
servers.hostname.memory.SwapTotal 262143996
servers.hostname.memory.VmallocChunk 34311049240
servers.hostname.memory.VmallocTotal 34359738367
servers.hostname.memory.VmallocUsed 445452
```

### This file was generated from the python source
### Please edit the source to make changes

