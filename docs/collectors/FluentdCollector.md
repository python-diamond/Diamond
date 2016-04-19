<!--This file was generated from the python source
Please edit the source to make changes
-->
FluentdCollector
=====

The FlutendCollector monitors fluentd and data about the kinesis stream.

#### Dependencies

 * flutend

#### Example config

```
    enabled = True
    host = localhost
    port = 24220
    [[[collect]]]
        kinesis = buffer_queue_length, buffer_total_queued_size, retry_count
```


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
collect | {} | Plugins and their metrics to collect | dict
enabled | False | Enable collecting these metrics | bool
host | localhost | Fluentd host | str
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
port | 24220 | Fluentd port | str

#### Example Output

```
__EXAMPLESHERE__
```

