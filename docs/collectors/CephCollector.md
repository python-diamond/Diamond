<!--This file was generated from the python source
Please edit the source to make changes
-->
CephCollector
=====

The CephCollector collects utilization info from the Ceph storage system.

Documentation for ceph perf counters:
http://ceph.com/docs/master/dev/perf_counters/

#### Dependencies

 * ceph [http://ceph.com/]


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
ceph_binary | /usr/bin/ceph | Path to "ceph" executable. Defaults to /usr/bin/ceph. | str
enabled | False | Enable collecting these metrics | bool
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
socket_ext | asok | Extension for socket filenames. Defaults to "asok" | str
socket_path | /var/run/ceph | The location of the ceph monitoring sockets. Defaults to "/var/run/ceph" | str
socket_prefix | ceph- | The first part of all socket names. Defaults to "ceph-" | str

#### Example Output

```
__EXAMPLESHERE__
```

