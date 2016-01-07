<!--This file was generated from the python source
Please edit the source to make changes
-->
DiskUsageCollector
=====

Collect IO Stats

Note: You may need to artificially generate some IO load on a disk/partition
before graphite will generate the metrics.

 * http://www.kernel.org/doc/Documentation/iostats.txt

#### Dependencies

 * /proc/diskstats


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
devices | PhysicalDrive[0-9]+$|md[0-9]+$|sd[a-z]+[0-9]*$|x?vd[a-z]+[0-9]*$|disk[0-9]+$|dm\-[0-9]+$ | A regex of which devices to gather metrics for. Defaults to md, sd, xvd, disk, and dm devices | str
enabled | False | Enable collecting these metrics | bool
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
sector_size | 512 | The size to use to calculate sector usage | int
send_zero | False | Send io data even when there is no io | bool

#### Example Output

```
servers.hostname.iostat.sda.average_queue_length 0.0
servers.hostname.iostat.sda.average_request_size_kilobyte 10.6
servers.hostname.iostat.sda.await 0.0
servers.hostname.iostat.sda.concurrent_io 0.0
servers.hostname.iostat.sda.io 3.0
servers.hostname.iostat.sda.io_in_progress 0.0
servers.hostname.iostat.sda.io_milliseconds 0.0
servers.hostname.iostat.sda.io_milliseconds_weighted 0.0
servers.hostname.iostat.sda.iops 0.3
servers.hostname.iostat.sda.read_kilobyte_per_second 0.0
servers.hostname.iostat.sda.read_requests_merged_per_second 0.0
servers.hostname.iostat.sda.reads 0.0
servers.hostname.iostat.sda.reads_kilobyte 0.0
servers.hostname.iostat.sda.reads_merged 0.0
servers.hostname.iostat.sda.reads_milliseconds 0.0
servers.hostname.iostat.sda.reads_per_second 0.0
servers.hostname.iostat.sda.service_time 0.0
servers.hostname.iostat.sda.util_percentage 0.0
servers.hostname.iostat.sda.write_kilobyte_per_second 3.2
servers.hostname.iostat.sda.write_requests_merged_per_second 0.5
servers.hostname.iostat.sda.writes 3.0
servers.hostname.iostat.sda.writes_kilobyte 32.0
servers.hostname.iostat.sda.writes_merged 5.0
servers.hostname.iostat.sda.writes_milliseconds 0.0
servers.hostname.iostat.sda.writes_per_second 0.3
servers.hostname.iostat.sdb.average_queue_length 0.7492
servers.hostname.iostat.sdb.average_request_size_kilobyte 6.3
servers.hostname.iostat.sdb.await 0.8
servers.hostname.iostat.sdb.concurrent_io 0.5
servers.hostname.iostat.sdb.io 9214.0
servers.hostname.iostat.sdb.io_in_progress 0.0
servers.hostname.iostat.sdb.io_milliseconds 4957.0
servers.hostname.iostat.sdb.io_milliseconds_weighted 7492.0
servers.hostname.iostat.sdb.iops 921.4
servers.hostname.iostat.sdb.read_kilobyte_per_second 1862.4
servers.hostname.iostat.sdb.read_requests_merged_per_second 0.0
servers.hostname.iostat.sdb.reads 1164.0
servers.hostname.iostat.sdb.reads_kilobyte 18624.0
servers.hostname.iostat.sdb.reads_merged 0.0
servers.hostname.iostat.sdb.reads_milliseconds 7163.0
servers.hostname.iostat.sdb.reads_per_second 116.4
servers.hostname.iostat.sdb.service_time 0.5
servers.hostname.iostat.sdb.util_percentage 49.57
servers.hostname.iostat.sdb.write_kilobyte_per_second 3914.3
servers.hostname.iostat.sdb.write_requests_merged_per_second 201.7
servers.hostname.iostat.sdb.writes 8050.0
servers.hostname.iostat.sdb.writes_kilobyte 39143.0
servers.hostname.iostat.sdb.writes_merged 2017.0
servers.hostname.iostat.sdb.writes_milliseconds 337.0
servers.hostname.iostat.sdb.writes_per_second 805.0
```

