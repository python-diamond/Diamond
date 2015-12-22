<!--This file was generated from the python source
Please edit the source to make changes
-->
MemoryCollector
=====

This class collects data on memory utilization

Note that MemFree may report no memory free. This may not actually be the case,
as memory is allocated to Buffers and Cache as well. See
[this link](http://www.linuxatemyram.com/) for more details.

#### Dependencies

* /proc/meminfo or psutil


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
detailed |  | Set to True to Collect all the nodes | 
enabled | False | Enable collecting these metrics | bool
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType

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

