<!--This file was generated from the python source
Please edit the source to make changes
-->
NetfilterAccountingCollector
=====

Collect counters from Netfilter accounting

#### Dependencies

 * [nfacct](http://www.netfilter.org/projects/nfacct/)


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
bin | nfacct | The path to the smartctl binary | str
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
reset | True | Reset counters after collecting | bool
sudo_cmd | /usr/bin/sudo | Path to sudo | str
use_sudo | False | Use sudo? | bool

#### Example Output

```
__EXAMPLESHERE__
```

