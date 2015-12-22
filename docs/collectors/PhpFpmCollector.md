<!--This file was generated from the python source
Please edit the source to make changes
-->
PhpFpmCollector
=====

Collects data from php-fpm if the pm.status_path is enabled


#### Usage

A sample php-fpm config for this collector to work is

```
pm.status_path = /fpm-status
```

#### Dependencies

 * urllib2
 * json (or simeplejson)


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte, | Default numeric output(s) | list
enabled | False | Enable collecting these metrics | bool
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType

#### Example Output

```
__EXAMPLESHERE__
```

