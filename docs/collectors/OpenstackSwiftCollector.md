<!--This file was generated from the python source
Please edit the source to make changes
-->
OpenstackSwiftCollector
=====

Openstack swift collector.

#### Dependencies

 * swift-dispersion-report commandline tool (for dispersion report)
   if using this, make sure swift.conf and dispersion.conf are readable by
   diamond also get an idea of the runtime of a swift-dispersion-report call
   and make sure the collect interval is high enough to avoid contention.
 * swift commandline tool (for container_metrics)

both of these should come installed with swift

#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
account |  | swift auth account (for enable_container_metrics) | 
auth_url |  | authentication url (for enable_container_metrics) | 
byte_unit | byte | Default numeric output(s) | str
containers |  | containers on which to count number of objects, space separated list (for enable_container_metrics) | 
enable_container_metrics | True | gather containers metrics (# objects, bytes used, x_timestamp. default True) | bool
enable_dispersion_report | False | gather swift-dispersion-report metrics (default False) | bool
enabled | False | Enable collecting these metrics | bool
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
password |  | swift auth password (for enable_container_metrics) | 
user |  | swift auth user (for enable_container_metrics) | 

#### Example Output

```
__EXAMPLESHERE__
```

