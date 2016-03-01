<!--This file was generated from the python source
Please edit the source to make changes
-->
HTTPJSONCollector
=====

Simple collector which get JSON and parse it into flat metrics

#### Dependencies

 * urllib2


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
headers | {'User-Agent': 'Diamond HTTP collector'} | Header variable if needed. Will be added to every request | dict
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
url | http://localhost/stat | Full URL | str

#### Example Output

```
__EXAMPLESHERE__
```

