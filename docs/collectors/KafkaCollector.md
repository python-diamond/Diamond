<!--This file was generated from the python source
Please edit the source to make changes
-->
KafkaCollector
=====

Collect stats via MX4J from Kafka

#### Dependencies

 * urllib2
 * xml.etree

#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
host | 127.0.0.1 |  | str
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
port | 8082 |  | int

#### Example Output

```
__EXAMPLESHERE__
```

