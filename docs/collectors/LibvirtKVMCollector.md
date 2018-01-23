<!--This file was generated from the python source
Please edit the source to make changes
-->
LibvirtKVMCollector
=====

Uses libvirt to harvest per KVM instance stats

#### Dependencies

 * python-libvirt, xml


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
cpu_absolute | False | CPU stats reported as percentage by default, or<br>as cummulative nanoseconds since VM creation if this is True. | bool
enabled | False | Enable collecting these metrics | bool
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
sort_by_uuid | False | Use the <uuid> of the instance instead of the<br> default <name>, useful in Openstack deploments where <name> is only<br> specific to the compute node | bool
uri | qemu:///system | The libvirt connection URI. By default it's<br>'qemu:///system'. One decent option is<br>'qemu+unix:///system?socket=/var/run/libvirt/libvit-sock-ro'. | str

#### Example Output

```
__EXAMPLESHERE__
```

