<!--This file was generated from the python source
Please edit the source to make changes
-->
WebsiteMonitorCollector
=====

Gather HTTP Response code and Duration of HTTP request

#### Dependencies
  * urllib2


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
URL |  | FQDN of HTTP endpoint to test | str
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType

#### Example Output

```
__EXAMPLESHERE__
```

