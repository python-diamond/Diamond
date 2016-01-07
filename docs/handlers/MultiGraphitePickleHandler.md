<!--This file was generated from the python source
Please edit the source to make changes
-->
MultiGraphitePickleHandler
====

Send metrics to a [graphite](http://graphite.wikidot.com/) using the pickle
interface. Unlike GraphitePickleHandler, this one supports multiple graphite
servers. Specify them as a list of hosts divided by comma.
#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
batch | 1 | How many to store before sending to the graphite server | int
get_default_config_help |  | get_default_config_help | 
host | localhost, | Hostname, Hostname, Hostname | list
max_backlog_multiplier | 5 | how many batches to store before trimming | int
port | 2003 | Port | int
proto | tcp | udp or tcp | str
server_error_interval | 120 | How frequently to send repeated server errors | int
timeout | 15 |  | int
trim_backlog_multiplier | 4 | Trim down how many batches | int
