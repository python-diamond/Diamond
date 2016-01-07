<!--This file was generated from the python source
Please edit the source to make changes
-->
ChronydCollector
=====

Collect metrics from chrony - http://chrony.tuxfamily.org/

#### Dependencies

 * subprocess


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
bin | /usr/bin/chronyc | The path to the chronyc binary | str
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
sudo_cmd | /usr/bin/sudo | Path to sudo | str
use_sudo | False | Use sudo? | bool

#### Example Output

```
servers.hostname.chrony.178_251_120_16.offset_ms -7e-05
servers.hostname.chrony.85_12_29_43.offset_ms -0.785
servers.hostname.chrony.85_234_197_3.offset_ms 0.08
servers.hostname.chrony.85_255_214_66.offset_ms 0.386
```

