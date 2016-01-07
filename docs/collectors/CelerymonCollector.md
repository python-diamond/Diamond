<!--This file was generated from the python source
Please edit the source to make changes
-->
CelerymonCollector
=====

Collects simple task stats out of a running celerymon process

#### Dependencies

 * celerymon connected to celery broker

Example config file CelerymonCollector.conf

```
enabled=True
host=celerymon.example.com
port=16379
```


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
host | localhost | A single hostname to get metrics from | str
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
path |  | celerymon | 
port | 8989 | The celerymon port | str

#### Example Output

```
__EXAMPLESHERE__
```

