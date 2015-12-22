<!--This file was generated from the python source
Please edit the source to make changes
-->
VMSFSCollector
=====

Uses /sys/fs/vmsfs to collect host-global data on VMS memory usage

#### Dependencies

 * /sys/fs/vmsfs <- vmsfs package, vmsfs mounted


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
__EXAMPLESHERE__
```

