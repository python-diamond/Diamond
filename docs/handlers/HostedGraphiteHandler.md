<!--This file was generated from the python source
Please edit the source to make changes
-->
HostedGraphiteHandler
====

[Hosted Graphite](https://www.hostedgraphite.com/) is the powerful open-source
application metrics system used by hundreds of companies. We take away the
headaches of scaling, maintenance, and upgrades and let you do what you do
best - write great software.

#### Configuration

Enable this handler

 * handlers = diamond.handler.hostedgraphite.HostedGraphiteHandler,

 * apikey = API_KEY

#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
apikey |  | Api key to use | str
batch | 1 | How many to store before sending to the graphite server | int
get_default_config_help |  | get_default_config_help | 
host | carbon.hostedgraphite.com | Hostname | str
max_backlog_multiplier | 5 | how many batches to store before trimming | int
port | 2003 | Port | int
proto | tcp | udp or tcp | str
server_error_interval | 120 | How frequently to send repeated server errors | int
timeout | 15 |  | int
trim_backlog_multiplier | 4 | Trim down how many batches | int
