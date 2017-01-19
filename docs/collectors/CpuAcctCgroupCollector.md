<!--This file was generated from the python source
Please edit the source to make changes
-->
CpuAcctCgroupCollector
=====

The CpuAcctCGroupCollector collects CPU Acct metric for cgroups

#### Dependencies

A mounted cgroup fs. Defaults to /sys/fs/cgroup/cpuacct/


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
path | /sys/fs/cgroup/cpuacct/ | Directory path to where cpuacct is located,<br>
defaults to /sys/fs/cgroup/cpuacct/. Redhat/CentOS/SL use /cgroup | str

#### Example Output

```
__EXAMPLESHERE__
```

