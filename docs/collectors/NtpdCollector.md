<!--This file was generated from the python source
Please edit the source to make changes
-->
NtpdCollector
=====

Collect stats from ntpd

#### Dependencies

    * subprocess


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
ntpdc_bin | /usr/bin/ntpdc | Path to ntpdc binary | str
ntpq_bin | /usr/bin/ntpq | Path to ntpq binary | str
sudo_cmd | /usr/bin/sudo | Path to sudo | str
use_sudo | False | Use sudo? | bool

#### Example Output

```
servers.hostname.ntpd.delay 0.127
servers.hostname.ntpd.est_error 5.1e-05
servers.hostname.ntpd.frequency -14.24
servers.hostname.ntpd.jitter 0.026
servers.hostname.ntpd.max_error 0.039793
servers.hostname.ntpd.offset -5.427e-06
servers.hostname.ntpd.poll 1024
servers.hostname.ntpd.reach 377
servers.hostname.ntpd.root_dispersion 0.09311
servers.hostname.ntpd.root_distance 0.07663
servers.hostname.ntpd.stratum 2
servers.hostname.ntpd.when 39
```

