<!--This file was generated from the python source
Please edit the source to make changes
-->
RRDHandler
====

Save stats in RRD files using rrdtool.
#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
basedir | /var/lib/collectd/rrd | The base directory for all RRD files. | str
batch | 1 | Wait for this many updates before saving to the RRD file | int
get_default_config_help |  | get_default_config_help | 
server_error_interval | 120 | How frequently to send repeated server errors | int
step | 10 | The minimum interval represented in generated RRD files. | int
