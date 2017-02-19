<!--This file was generated from the python source
Please edit the source to make changes
-->
MdStatCollector
=====

Collect linux RAID/md state by parsing /proc/mdstat.
https://raid.wiki.kernel.org/index.php/Mdstat

#### Dependencies

 * /proc/mdstat


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
servers.hostname.mdstat.md0.bitmap.allocated_pages 1
servers.hostname.mdstat.md0.bitmap.chunk_size 65536
servers.hostname.mdstat.md0.bitmap.page_size 4
servers.hostname.mdstat.md0.bitmap.total_pages 1
servers.hostname.mdstat.md0.member_count.active 2
servers.hostname.mdstat.md0.member_count.faulty 0
servers.hostname.mdstat.md0.member_count.spare 0
servers.hostname.mdstat.md0.recovery.percent 99.5
servers.hostname.mdstat.md0.recovery.remaining_time 802199
servers.hostname.mdstat.md0.recovery.speed 104726528
servers.hostname.mdstat.md0.status.actual_members 1
servers.hostname.mdstat.md0.status.blocks 102272
servers.hostname.mdstat.md0.status.superblock_version 1.2
servers.hostname.mdstat.md0.status.total_members 2
```
