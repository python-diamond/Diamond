<!--This file was generated from the python source
Please edit the source to make changes
-->
MySQLPerfCollector
=====


Diamond collector that monitors relevant MySQL performance_schema values
For now only monitors replication load

[Blog](http://bit.ly/PbSkbN) announcement.

[Snippet](http://bit.ly/SHwYhT) to build example graph.

#### Dependencies

 * MySQLdb
 * MySQL 5.5.3+


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
hosts | , | List of hosts to collect from. Format is yourusername:yourpassword@host:port/performance_schema[/nickname] | list
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
slave | False | Collect Slave Replication Metrics | str

#### Example Output

```
__EXAMPLESHERE__
```

