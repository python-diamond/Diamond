<!--This file was generated from the python source
Please edit the source to make changes
-->
BeanstalkdCollector
=====

Collects the following from beanstalkd:
    - Server statistics via the 'stats' command
    - Per tube statistics via the 'stats-tube' command

#### Dependencies

 * beanstalkc


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
host | localhost | Hostname | str
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
port | 11300 | Port | int

#### Example Output

```
__EXAMPLESHERE__
```

