<!--This file was generated from the python source
Please edit the source to make changes
-->
TwemproxyCollector
=====

Collect twemproxy (aka nutcracker) stats ( Modified from memcached collector )

#### Dependencies

 * json or simplejson

#### Example Configuration

TwemproxyCollector.conf

```
    enabled = True
    hosts = localhost:22222, app-1@localhost:22222, app-2@localhost:22222, etc
```

TO use a unix socket, set a host string like this

```
    hosts = /path/to/blah.sock, app-1@/path/to/bleh.sock,
```

#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
hosts | localhost:22222, | List of hosts, and ports to collect. Set an alias by  prefixing the host:port with alias@ | list
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType

#### Example Output

```
servers.hostname.twemproxy.localhost.curr_connections 5
servers.hostname.twemproxy.localhost.pools.development.client_connections 358
servers.hostname.twemproxy.localhost.pools.development.client_eof 2.0
servers.hostname.twemproxy.localhost.pools.development.client_err 2.51666666667
servers.hostname.twemproxy.localhost.pools.development.forward_error 0
servers.hostname.twemproxy.localhost.pools.development.fragments 376.8
servers.hostname.twemproxy.localhost.pools.development.server_ejects 0
servers.hostname.twemproxy.localhost.pools.development.servers.127_0_0_95.in_queue 0
servers.hostname.twemproxy.localhost.pools.development.servers.127_0_0_95.in_queue_bytes 0
servers.hostname.twemproxy.localhost.pools.development.servers.127_0_0_95.out_queue 0
servers.hostname.twemproxy.localhost.pools.development.servers.127_0_0_95.out_queue_bytes 0
servers.hostname.twemproxy.localhost.pools.development.servers.127_0_0_95.request_bytes 817584.066667
servers.hostname.twemproxy.localhost.pools.development.servers.127_0_0_95.requests 215.883333333
servers.hostname.twemproxy.localhost.pools.development.servers.127_0_0_95.response_bytes 61628.6833333
servers.hostname.twemproxy.localhost.pools.development.servers.127_0_0_95.responses 215.75
servers.hostname.twemproxy.localhost.pools.development.servers.127_0_0_95.server_connections 100
servers.hostname.twemproxy.localhost.pools.development.servers.127_0_0_95.server_eof 0
servers.hostname.twemproxy.localhost.pools.development.servers.127_0_0_95.server_err 0
servers.hostname.twemproxy.localhost.pools.development.servers.127_0_0_95.server_timedout 0
servers.hostname.twemproxy.localhost.pools.development.servers.127_0_0_96.in_queue 0
servers.hostname.twemproxy.localhost.pools.development.servers.127_0_0_96.in_queue_bytes 0
servers.hostname.twemproxy.localhost.pools.development.servers.127_0_0_96.out_queue 0
servers.hostname.twemproxy.localhost.pools.development.servers.127_0_0_96.out_queue_bytes 0
servers.hostname.twemproxy.localhost.pools.development.servers.127_0_0_96.request_bytes 357937.55
servers.hostname.twemproxy.localhost.pools.development.servers.127_0_0_96.requests 229.2
servers.hostname.twemproxy.localhost.pools.development.servers.127_0_0_96.response_bytes 84637.3666667
servers.hostname.twemproxy.localhost.pools.development.servers.127_0_0_96.responses 229.166666667
servers.hostname.twemproxy.localhost.pools.development.servers.127_0_0_96.server_connections 100
servers.hostname.twemproxy.localhost.pools.development.servers.127_0_0_96.server_eof 1.66666666667
servers.hostname.twemproxy.localhost.pools.development.servers.127_0_0_96.server_err 0
servers.hostname.twemproxy.localhost.pools.development.servers.127_0_0_96.server_timedout 0
servers.hostname.twemproxy.localhost.pools.production.client_connections 358
servers.hostname.twemproxy.localhost.pools.production.client_eof 2.0
servers.hostname.twemproxy.localhost.pools.production.client_err 2.51666666667
servers.hostname.twemproxy.localhost.pools.production.forward_error 0
servers.hostname.twemproxy.localhost.pools.production.fragments 376.8
servers.hostname.twemproxy.localhost.pools.production.server_ejects 0
servers.hostname.twemproxy.localhost.pools.production.servers.127_0_0_92.in_queue 0
servers.hostname.twemproxy.localhost.pools.production.servers.127_0_0_92.in_queue_bytes 0
servers.hostname.twemproxy.localhost.pools.production.servers.127_0_0_92.out_queue 0
servers.hostname.twemproxy.localhost.pools.production.servers.127_0_0_92.out_queue_bytes 0
servers.hostname.twemproxy.localhost.pools.production.servers.127_0_0_92.request_bytes 631888.916667
servers.hostname.twemproxy.localhost.pools.production.servers.127_0_0_92.requests 229.35
servers.hostname.twemproxy.localhost.pools.production.servers.127_0_0_92.response_bytes 56435.1833333
servers.hostname.twemproxy.localhost.pools.production.servers.127_0_0_92.responses 229.25
servers.hostname.twemproxy.localhost.pools.production.servers.127_0_0_92.server_connections 100
servers.hostname.twemproxy.localhost.pools.production.servers.127_0_0_92.server_eof 0
servers.hostname.twemproxy.localhost.pools.production.servers.127_0_0_92.server_err 0
servers.hostname.twemproxy.localhost.pools.production.servers.127_0_0_92.server_timedout 0
servers.hostname.twemproxy.localhost.pools.production.servers.127_0_0_93.in_queue 1
servers.hostname.twemproxy.localhost.pools.production.servers.127_0_0_93.in_queue_bytes 38
servers.hostname.twemproxy.localhost.pools.production.servers.127_0_0_93.out_queue 0
servers.hostname.twemproxy.localhost.pools.production.servers.127_0_0_93.out_queue_bytes 0
servers.hostname.twemproxy.localhost.pools.production.servers.127_0_0_93.request_bytes 939547.333333
servers.hostname.twemproxy.localhost.pools.production.servers.127_0_0_93.requests 280.433333333
servers.hostname.twemproxy.localhost.pools.production.servers.127_0_0_93.response_bytes 246464.15
servers.hostname.twemproxy.localhost.pools.production.servers.127_0_0_93.responses 280.283333333
servers.hostname.twemproxy.localhost.pools.production.servers.127_0_0_93.server_connections 100
servers.hostname.twemproxy.localhost.pools.production.servers.127_0_0_93.server_eof 0
servers.hostname.twemproxy.localhost.pools.production.servers.127_0_0_93.server_err 0
servers.hostname.twemproxy.localhost.pools.production.servers.127_0_0_93.server_timedout 0.716666666667
servers.hostname.twemproxy.localhost.pools.production.servers.127_0_0_94.in_queue 0
servers.hostname.twemproxy.localhost.pools.production.servers.127_0_0_94.in_queue_bytes 0
servers.hostname.twemproxy.localhost.pools.production.servers.127_0_0_94.out_queue 0
servers.hostname.twemproxy.localhost.pools.production.servers.127_0_0_94.out_queue_bytes 0
servers.hostname.twemproxy.localhost.pools.production.servers.127_0_0_94.request_bytes 413543.0
servers.hostname.twemproxy.localhost.pools.production.servers.127_0_0_94.requests 247.1
servers.hostname.twemproxy.localhost.pools.production.servers.127_0_0_94.response_bytes 361848.85
servers.hostname.twemproxy.localhost.pools.production.servers.127_0_0_94.responses 247.083333333
servers.hostname.twemproxy.localhost.pools.production.servers.127_0_0_94.server_connections 100
servers.hostname.twemproxy.localhost.pools.production.servers.127_0_0_94.server_eof 0
servers.hostname.twemproxy.localhost.pools.production.servers.127_0_0_94.server_err 0
servers.hostname.twemproxy.localhost.pools.production.servers.127_0_0_94.server_timedout 0
servers.hostname.twemproxy.localhost.total_connections 4.85
servers.hostname.twemproxy.localhost.uptime 703137
```

