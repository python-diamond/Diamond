<!--This file was generated from the python source
Please edit the source to make changes
-->
ConnTrackCollector
=====

Collecting connections tracking statistics from nf_conntrack/ip_conntrack
kernel module.

#### Dependencies

 * nf_conntrack/ip_conntrack kernel module


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
dir | /proc/sys/net/ipv4/netfilter,/proc/sys/net/netfilter | Directories with files of interest, comma seperated | str
enabled | False | Enable collecting these metrics | bool
files | ip_conntrack_count,ip_conntrack_max,nf_conntrack_count,nf_conntrack_max | List of files to collect statistics from | str
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType

#### Example Output

```
servers.hostname.conntrack.ip_conntrack_count 33.0
servers.hostname.conntrack.ip_conntrack_max 36.0
```

