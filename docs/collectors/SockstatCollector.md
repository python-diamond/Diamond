<!--This file was generated from the python source
Please edit the source to make changes
-->
SockstatCollector
=====

Uses /proc/net/sockstat to collect data on number of open sockets

#### Dependencies

 * /proc/net/sockstat


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType

#### Example Output

```
servers.hostname.sockets.tcp_alloc 13
servers.hostname.sockets.tcp_inuse 61
servers.hostname.sockets.tcp_mem 1
servers.hostname.sockets.tcp_orphan 0
servers.hostname.sockets.tcp_tw 1
servers.hostname.sockets.udp_inuse 6
servers.hostname.sockets.udp_mem 0
servers.hostname.sockets.used 118
```

