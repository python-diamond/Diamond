<!--This file was generated from the python source
Please edit the source to make changes
-->
InfluxdbHandler
====

Send metrics to a [influxdb](https://github.com/influxdb/influxdb/) using the
http interface.

v1.0 : creation
v1.1 : force influxdb driver with SSL
v1.2 : added a timer to delay influxdb writing in case of failure
       this whill avoid the 100% cpu loop when influx in not responding
       Sebastien Prune THOMAS - prune@lecentre.net

#### Dependencies
 * [influxdb](https://github.com/influxdb/influxdb-python)


#### Configuration
```
[[InfluxdbHandler]]
hostname = localhost
port = 8086 #8084 for HTTPS
batch_size = 100 # default to 1
cache_size = 1000 # default to 20000
username = root
password = root
database = graphite
time_precision = s
```
#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
batch_size | 1 | How many metrics to store before sending to the influxdb server | int
cache_size | 20000 | How many values to store in cache in case of influxdb failure | int
database | graphite | Database name | str
get_default_config_help |  | get_default_config_help | 
hostname | localhost | Hostname | str
password | root | Password for connection | str
port | 8086 | Port | int
server_error_interval | 120 | How frequently to send repeated server errors | int
ssl | False | set to True to use HTTPS instead of http | bool
time_precision | s | time precision in second(s), milisecond(ms) or microsecond (u) | str
username | root | Username for connection | str
