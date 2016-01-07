<!--This file was generated from the python source
Please edit the source to make changes
-->
EximCollector
=====

Shells out to get the exim queue length

#### Dependencies

 * /usr/sbin/exim


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
bin | /usr/sbin/exim | The path to the exim binary | str
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
sudo_cmd | /usr/bin/sudo | Path to sudo | str
sudo_user | root | User to sudo as | str
use_sudo | False | Use sudo? | bool

#### Example Output

```
servers.hostname.exim.queuesize 33.0
```

