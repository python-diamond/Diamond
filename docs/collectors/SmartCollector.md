<!--This file was generated from the python source
Please edit the source to make changes
-->
SmartCollector
=====

Collect data from S.M.A.R.T.'s attribute reporting.

#### Dependencies

 * [smartmontools](https://www.smartmontools.org)


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
aliases | {} | Aliases to assign | dict
attributes | {} | Attributes to publish | dict
bin | smartctl | The path to the smartctl binary | str
byte_unit | byte | Default numeric output(s) | str
devices | ^disk[0-9]$|^sd[a-z]$|^hd[a-z]$ | Devices to collect stats on (regexp) | str
enabled | False | Enable collecting these metrics | bool
force_prefails | False | If True, fetches all attributes with pre-fail priority and "attributes" specified in config. Otherwise, only "attributes" will be fetched. | bool
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
sudo_cmd | /usr/bin/sudo | Path to sudo | str
use_sudo | False | Use sudo? | bool
valtypes | value, worst, thresh, raw_val, | Values to publish | list

#### Example Output

```
servers.hostname.smart.sda.pre-fail.raw_read_error_rate.value 100
servers.hostname.smart.sda.pre-fail.raw_read_error_rate.worst 100
servers.hostname.smart.sda.pre-fail.raw_read_error_rate.thresh 16
servers.hostname.smart.sda.pre-fail.raw_read_error_rate.raw_val  0
servers.hostname.smart.sda.pre-fail.throughput_performance.value 138
servers.hostname.smart.sda.pre-fail.throughput_performance.worst 138
servers.hostname.smart.sda.pre-fail.throughput_performance.thresh 54
servers.hostname.smart.sda.pre-fail.throughput_performance.raw_val 100
servers.hostname.smart.sda.old-age.start_stop_count.value 100
servers.hostname.smart.sda.old-age.start_stop_count.worst 100
servers.hostname.smart.sda.old-age.start_stop_count.thresh 0
servers.hostname.smart.sda.old-age.start_stop_count.raw_val 11
servers.hostname.smart.sda.pre-fail.some_attribute.value 153
servers.hostname.smart.sda.pre-fail.some_attribute.worst 153
servers.hostname.smart.sda.pre-fail.some_attribute.thresh 24
servers.hostname.smart.sda.pre-fail.some_attribute.raw_val 396
```
