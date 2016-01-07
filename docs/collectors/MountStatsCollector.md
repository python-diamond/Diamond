<!--This file was generated from the python source
Please edit the source to make changes
-->
MountStatsCollector
=====

The function of MountStatsCollector is to parse the detailed per-mount NFS
performance statistics provided by `/proc/self/mountstats` (reads, writes,
remote procedure call count/latency, etc.) and provide counters to Diamond.
Filesystems may be included/excluded using a regular expression filter,
like the existing disk check collectors.

#### Dependencies

 * /proc/self/mountstats


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
exclude_filters | , | A list of regex patterns. Any filesystem matching any of these patterns will be excluded from mount stats metrics collection. | list
include_filters | , | A list of regex patterns. Any filesystem matching any of these patterns will be included from mount stats metrics collection. | list
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
sudo_cmd | /usr/bin/sudo | Path to sudo | str
use_sudo | False | Use sudo? | bool

#### Example Output

```
__EXAMPLESHERE__
```

