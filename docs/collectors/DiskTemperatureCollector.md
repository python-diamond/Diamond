<!--This file was generated from the python source
Please edit the source to make changes
-->
DiskTemperatureCollector
=====

Collect disk temperature with S.M.A.R.T.

This collector use hddtemp to collect only the disk temperature from the disk
S.M.A.R.T information. This can be faster than smartctl since it only extracts
a single value.

#### Dependencies

 * [hddtemp](http://www.guzu.net/linux/hddtemp.php)


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
bin | hddtemp | The path to the hddtemp binary | str
byte_unit | byte | Default numeric output(s) | str
devices | ^disk[0-9]$|^sd[a-z]$|^hd[a-z]$ | device regex to collect stats on | str
enabled | False | Enable collecting these metrics | bool
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
sudo_cmd | /usr/bin/sudo | Path to sudo | str
use_sudo | False | Use sudo? | bool

#### Example Output

```
__EXAMPLESHERE__
```

