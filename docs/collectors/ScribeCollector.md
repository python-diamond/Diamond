<!--This file was generated from the python source
Please edit the source to make changes
-->
ScribeCollector
=====

Collect counters from scribe

#### Dependencies

    * /usr/sbin/scribe_ctrl, distributed with scribe


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
scribe_ctrl_bin | /usr/sbin/scribe_ctrl | Path to scribe_ctrl binary | str
scribe_port | None | Scribe port | NoneType

#### Example Output

```
__EXAMPLESHERE__
```

