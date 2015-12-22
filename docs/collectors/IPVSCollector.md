<!--This file was generated from the python source
Please edit the source to make changes
-->
IPVSCollector
=====

Shells out to get ipvs statistics, which may or may not require sudo access

#### Dependencies

 * /usr/sbin/ipvsadmin


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
bin | /usr/sbin/ipvsadm | Path to ipvsadm binary | str
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
sudo_cmd | /usr/bin/sudo | Path to sudo | str
use_sudo | True | Use sudo? | bool

#### Example Output

```
servers.hostname.ipvs.TCP_172_16_1_56:443.10_68_15_66:443.conns 59
servers.hostname.ipvs.TCP_172_16_1_56:443.10_68_15_66:443.outbytes 216873
servers.hostname.ipvs.TCP_172_16_1_56:443.total.conns 59
servers.hostname.ipvs.TCP_172_16_1_56:80.total.conns 116
```

