<!--This file was generated from the python source
Please edit the source to make changes
-->
GraphiteHandler
====

Send metrics to a [graphite](http://graphite.wikidot.com/) using the high
performace pickle interface.

Graphite is an enterprise-scale monitoring tool that runs well on cheap
hardware. It was originally designed and written by Chris Davis at Orbitz in
2006 as side project that ultimately grew to be a foundational monitoring tool.
In 2008, Orbitz allowed Graphite to be released under the open source Apache
2.0 license. Since then Chris has continued to work on Graphite and has
deployed it at other companies including Sears, where it serves as a pillar of
the e-commerce monitoring system. Today many
[large companies](http://graphite.readthedocs.org/en/latest/who-is-using.html)
use it.

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
port | 2003 | Port | int
proto | tcp | udp, udp4, udp6, tcp, tcp4, or tcp6 | str
scope_id | 0 | IPv6 Scope ID | int
server_error_interval | 120 | How frequently to send repeated server errors | int
timeout | 15 |  | int
trim_backlog_multiplier | 4 | Trim down how many batches | int
