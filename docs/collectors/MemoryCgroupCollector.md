<!--This file was generated from the python source
Please edit the source to make changes
-->
MemoryCgroupCollector
=====

The MemoryCgroupCollector collects memory metric for cgroups

Example config:

```
memory_path=/sys/fs/cgroup/memory/
skip=group\d+,mygroup\d\d
enabled=True
```

memory_path -- path to CGroups memory stat
skip -- comma-separated list of regexps, which paths should we skip

Stats that we are interested in tracking:

cache - # of bytes of page cache memory.
rss   - # of bytes of anonymous and swap cache memory.
swap  - # of bytes of swap usage

Metrics with total_ prefixes - summarized data from children CGroups.

#### Dependencies

/sys/fs/cgroup/memory/memory.stat

#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType

#### Example Output

```
__EXAMPLESHERE__
```

