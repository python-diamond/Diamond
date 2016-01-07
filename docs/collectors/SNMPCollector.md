<!--This file was generated from the python source
Please edit the source to make changes
-->
SNMPCollector
=====

SNMPCollector is a special collector for collecting data by using SNMP

#### Dependencies

 * pysnmp


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
retries | 3 | Number of times to retry before bailing | int
timeout | 5 | Seconds before timing out the snmp connection | int

#### Example Output

```
__EXAMPLESHERE__
```

