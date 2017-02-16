<!--This file was generated from the python source
Please edit the source to make changes
-->
GlusterFSCollector
=====

The GlusterFSCollector currently only collects latency percentages
from the GlusterFS storage system.

version 0.3 beta

Documentation for GlusterFS profiling:
http://gluster.readthedocs.org/en/latest/Administrator%20Guide/Monitoring%20Workload/

#### Dependencies

 * glusterfs [https://www.gluster.org/]
 * Profiling enabled: gluster volume profile <VOLNAME> start


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
gluster_path | /usr/sbin/gluster | complete path to gluster binary. | str
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
target_brick |  | which node/server to send metrics for. Defaults to all | str
target_volume |  | which brick to send info on. Defaults to all | str

#### Example Output

```
__EXAMPLESHERE__
```

