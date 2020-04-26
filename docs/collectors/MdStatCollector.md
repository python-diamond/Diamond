<!--This file was generated from the python source
Please edit the source to make changes
-->
MdStatCollector
=====

Collect linux RAID/md state by parsing /proc/mdstat.
<https://raid.wiki.kernel.org/index.php/Mdstat>

#### Dependencies

- /proc/mdstat

#### Supported metrics

```
md0 : active raid1 sda1[0] sda2[2](S) sda3[1]
```
- member_count.active
- member_count.faulty
- member_count.spare

```
39058432 blocks super 1.2 level 5, 512k chunk, algorithm 2 [3/3] [UUU]
199800 blocks super 1.2 999k rounding
```
- status.blocks
- status.superblock_version
- status.raid_level
- status.chunk_size
- status.algorithm
- status.rounding_factor
- status.actual_members
- status.total_members

```
bitmap: 1/1 pages [4KB], 65536KB chunk
```
- bitmap.total_pages
- bitmap.allocated_pages
- bitmap.page_size

```
[===================>.]  recovery = 99.5% (102272/102272) finish=13.37min
                         speed=102272K/sec
```
- recovery.percent
- recovery.speed
- recovery.remaining_time

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
