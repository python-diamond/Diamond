<!--This file was generated from the python source
Please edit the source to make changes
-->
KSMCollector
=====

This class collects 'Kernel Samepage Merging' statistics.
KSM is a memory de-duplication feature of the Linux Kernel (2.6.32+).

It can be enabled, if compiled into your kernel, by echoing 1 to
/sys/kernel/mm/ksm/run. You can find more information about KSM at
[http://www.linux-kvm.org/page/KSM](http://www.linux-kvm.org/page/KSM).

#### Dependencies

 * KSM built into your kernel. It does not have to be enabled, but the stats
 will be less than useful if it isn't:-)


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
ksm_path | /sys/kernel/mm/ksm | location where KSM kernel data can be found | str
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType

#### Example Output

```
servers.hostname.ksm.full_scans 123.0
servers.hostname.ksm.pages_shared 124.0
servers.hostname.ksm.pages_sharing 125.0
servers.hostname.ksm.pages_to_scan 100.0
servers.hostname.ksm.pages_unshared 126.0
servers.hostname.ksm.pages_volatile 127.0
servers.hostname.ksm.run 1.0
servers.hostname.ksm.sleep_millisecs 20.0
```

