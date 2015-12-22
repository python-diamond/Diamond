<!--This file was generated from the python source
Please edit the source to make changes
-->
GraphitePickleHandler
====

Send metrics to a [graphite](http://graphite.wikidot.com/) using the pickle
interface. Unlike GraphitePickleHandler, this one supports multiple graphite
servers. Specify them as a list of hosts divided by comma.
#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
batch | 1 | How many to store before sending to the graphite server | int
flow_info | 0 | IPv6 Flow Info | int
get_default_config_help |  | get_default_config_help | 
host | localhost | Hostname | str
keepalive | 0 | Enable keepalives for tcp streams | int
keepaliveinterval | 10 | How frequently to send keepalives | int
max_backlog_multiplier | 5 | how many batches to store before trimming | int
port | 2004 | Port | int
proto | tcp | udp, udp4, udp6, tcp, tcp4, or tcp6 | str
scope_id | 0 | IPv6 Scope ID | int
server_error_interval | 120 | How frequently to send repeated server errors | int
timeout | 15 |  | int
trim_backlog_multiplier | 4 | Trim down how many batches | int
