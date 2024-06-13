<!--This file was generated from the python source
Please edit the source to make changes
-->
CPUCollector
=====

The CPUCollector collects CPU utilization metric using /proc/stat.

#### Dependencies

 * /proc/stat


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
extended | False | return aggregate CPU% metric and complex CPU metrics | str
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
normalize | False | for cpu totals, divide by the number of CPUs | str
percore | True | Collect metrics per cpu core or just total | str
simple | False | only return aggregate CPU% metric | str

#### Example Output

```
servers.hostname.cpu.total.idle 2440.8
servers.hostname.cpu.total.iowait 0.2
servers.hostname.cpu.total.nice 0.0
servers.hostname.cpu.total.system 0.2
servers.hostname.cpu.total.user 0.4
```
