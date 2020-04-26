<!--This file was generated from the python source
Please edit the source to make changes
-->
NtpCollector
=====

Collect out of band stats from ntp

Uses output from ntpdate:

```
$ ntpdate -q pool.ntp.org
server 12.34.56.1, stratum 2, offset -0.000277, delay 0.02878
server 12.34.56.2, stratum 1, offset -0.000128, delay 0.02896
server 12.34.56.3, stratum 2, offset 0.000613, delay 0.02870
server 12.34.56.4, stratum 2, offset -0.000351, delay 0.02864
31 Apr 12:00:00 ntpdate[12]: adjust time server 12.34.56.2 offset -0.000128 sec
$
```

#### Dependencies

    * /usr/sbin/ntpdate
    * subprocess


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
bin | /usr/sbin/ntpdate | Path to ntpdate binary | str
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
ntp_pool | pool.ntp.org | NTP Pool address | str
precision | 0 | Number of decimal places to report to | int
sudo_cmd | /usr/bin/sudo | Path to sudo | str
time_scale | milliseconds | Time unit to report offset in | str
use_sudo | False | Use sudo? | bool

#### Example Output

```
servers.hostname.ntp.offset.milliseconds 0
servers.hostname.ntp.server.count 4
```

