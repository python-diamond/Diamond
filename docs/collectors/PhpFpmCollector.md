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

If the URL of the fpm-status page is http://127.0.0.1:8080/fpm-status, you need to set:

```
enabled = True
host = 127.0.0.1
port = 8080
uri = fpm-status
```

#### Dependencies

 * urllib2
 * json (or simeplejson)


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte, | Default numeric output(s) | list
enabled | False | Enable collecting these metrics | bool
host | localhost | Host part of the URL | string
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
port | 80 | Port part of the URL | int
uri | fpm-status | Path part of the URL, with or without the leading / | string

#### Example Output

```
__EXAMPLESHERE__
```

