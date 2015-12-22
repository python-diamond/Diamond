<!--This file was generated from the python source
Please edit the source to make changes
-->
TokuMXCollector
=====

Collects all number values from the db.serverStatus() and db.engineStatus()
command, other values are ignored.

#### Dependencies

 * pymongo


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
databases | .* | A regex of which databases to gather metrics for. Defaults to all databases. | str
enabled | False | Enable collecting these metrics | bool
host |  | A single hostname(:port) to get metrics from (can be used instead of hosts and overrides it) | 
hosts | localhost, | Array of hostname(:port) elements to get metrics fromSet an alias by prefixing host:port with alias@ | list
ignore_collections | ^tmp\.mr\. | A regex of which collections to ignore. MapReduce temporary collections (tmp.mr.*) are ignored by default. | str
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
network_timeout | None | Timeout for mongodb connection (in seconds). There is no timeout by default. | NoneType
passwd | None | Password for authenticated login (optional) | NoneType
simple | False | Only collect the same metrics as mongostat. | str
translate_collections | False | Translate dot (.) to underscores (_) in collection names. | str
user | None | Username for authenticated login (optional) | NoneType

#### Example Output

```
__EXAMPLESHERE__
```

