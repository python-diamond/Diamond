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

#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>byte_unit</td><td>byte</td><td>Default numeric output(s)</td><td>str</td></tr>
<tr><td>enabled</td><td>False</td><td>Enable collecting these metrics</td><td>bool</td></tr>
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

