InfluxdbHandler
====

Send metrics to a [influxdb](https://github.com/influxdb/influxdb/) using the
http interface.

v1.0 : creation
v1.1 : force influxdb driver with SSL
v1.2 : added a timer to delay influxdb writing in case of failure
       this whill avoid the 100% cpu loop when influx in not responding
       Sebastien Prune THOMAS - prune@lecentre.net

- Dependency:
    - influxdb client (pip install influxdb)
      you need version > 0.1.6 for HTTPS (not yet released)

- enable it in `diamond.conf` :

handlers = diamond.handler.influxdbHandler.InfluxdbHandler

- add config to `diamond.conf` :

[[InfluxdbHandler]]
hostname = localhost
port = 8086 #8084 for HTTPS
batch_size = 100 # default to 1
cache_size = 1000 # default to 20000
username = root
password = root
database = graphite
time_precision = s
#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>batch_size</td><td>1</td><td>How many metrics to store before sending to the influxdb server</td><td>int</td></tr>
<tr><td>cache_size</td><td>20000</td><td>How many values to store in cache in case of influxdb failure</td><td>int</td></tr>
<tr><td>database</td><td>graphite</td><td>Database name</td><td>str</td></tr>
<tr><td>get_default_config_help</td><td></td><td>get_default_config_help</td><td></td></tr>
<tr><td>hostname</td><td>localhost</td><td>Hostname</td><td>str</td></tr>
<tr><td>password</td><td>root</td><td>Password for connection</td><td>str</td></tr>
<tr><td>port</td><td>8086</td><td>Port</td><td>int</td></tr>
<tr><td>server_error_interval</td><td>120</td><td>How frequently to send repeated server errors</td><td>int</td></tr>
<tr><td>ssl</td><td>False</td><td>set to True to use HTTPS instead of http</td><td>bool</td></tr>
<tr><td>time_precision</td><td>s</td><td>time precision in second(s), milisecond(ms) or microsecond (u)</td><td>str</td></tr>
<tr><td>username</td><td>root</td><td>Username for connection</td><td>str</td></tr>
</table>

### This file was generated from the python source
### Please edit the source to make changes

