<!--This file was generated from the python source
Please edit the source to make changes
-->
SquidCollector
=====

Collects data from squid servers

#### Dependencies


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
hosts | localhost:3128, | List of hosts to collect from. Format is [nickname@]host[:port], [nickname@]host[:port], etc | list
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType

#### Example Output

```
servers.hostname.squid.3128.aborted_requests 0
servers.hostname.squid.3128.cd.kbytes_recv 0
servers.hostname.squid.3128.cd.kbytes_sent 0
servers.hostname.squid.3128.cd.local_memory 0
servers.hostname.squid.3128.cd.memory 0
servers.hostname.squid.3128.cd.msgs_recv 0
servers.hostname.squid.3128.cd.msgs_sent 0
servers.hostname.squid.3128.cd.times_used 0
servers.hostname.squid.3128.client_http.errors 0
servers.hostname.squid.3128.client_http.hit_kbytes_out 10
servers.hostname.squid.3128.client_http.hits 1
servers.hostname.squid.3128.client_http.kbytes_in 1
servers.hostname.squid.3128.client_http.kbytes_out 12.0
servers.hostname.squid.3128.client_http.requests 2
servers.hostname.squid.3128.cpu_time 0
servers.hostname.squid.3128.icp.kbytes_recv 0
servers.hostname.squid.3128.icp.kbytes_sent 0
servers.hostname.squid.3128.icp.pkts_recv 0
servers.hostname.squid.3128.icp.pkts_sent 0
servers.hostname.squid.3128.icp.q_kbytes_recv 0
servers.hostname.squid.3128.icp.q_kbytes_sent 0
servers.hostname.squid.3128.icp.queries_recv 0
servers.hostname.squid.3128.icp.queries_sent 0
servers.hostname.squid.3128.icp.query_timeouts 0
servers.hostname.squid.3128.icp.r_kbytes_recv 0
servers.hostname.squid.3128.icp.r_kbytes_sent 0
servers.hostname.squid.3128.icp.replies_queued 0
servers.hostname.squid.3128.icp.replies_recv 0
servers.hostname.squid.3128.icp.replies_sent 0
servers.hostname.squid.3128.icp.times_used 0
servers.hostname.squid.3128.page_faults 0
servers.hostname.squid.3128.select_loops 10827.0
servers.hostname.squid.3128.server.all.errors 0
servers.hostname.squid.3128.server.all.kbytes_in 0
servers.hostname.squid.3128.server.all.kbytes_out 0
servers.hostname.squid.3128.server.all.requests 0
servers.hostname.squid.3128.server.ftp.errors 0
servers.hostname.squid.3128.server.ftp.kbytes_in 0
servers.hostname.squid.3128.server.ftp.kbytes_out 0
servers.hostname.squid.3128.server.ftp.requests 0
servers.hostname.squid.3128.server.http.errors 0
servers.hostname.squid.3128.server.http.kbytes_in 0
servers.hostname.squid.3128.server.http.kbytes_out 0
servers.hostname.squid.3128.server.http.requests 0
servers.hostname.squid.3128.server.other.errors 0
servers.hostname.squid.3128.server.other.kbytes_in 0
servers.hostname.squid.3128.server.other.kbytes_out 0
servers.hostname.squid.3128.server.other.requests 0
servers.hostname.squid.3128.swap.files_cleaned 0
servers.hostname.squid.3128.swap.ins 2
servers.hostname.squid.3128.swap.outs 0
servers.hostname.squid.3128.unlink.requests 0
servers.hostname.squid.3128.wall_time 10
```

