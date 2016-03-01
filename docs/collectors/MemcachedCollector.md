<!--This file was generated from the python source
Please edit the source to make changes
-->
MemcachedCollector
=====

Collect memcached stats



#### Dependencies

 * subprocess

#### Example Configuration

MemcachedCollector.conf

```
    enabled = True
    hosts = localhost:11211, app-1@localhost:11212, app-2@localhost:11213, etc
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
hosts | localhost:11211, | List of hosts, and ports to collect. Set an alias by  prefixing the host:port with alias@ | list
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
publish |  | Which rows of 'status' you would like to publish. Telnet host port' and type stats and hit enter to see the list of possibilities. Leave unset to publish all. | 

#### Example Output

```
servers.hostname.memcached.localhost.auth_cmds 0.0
servers.hostname.memcached.localhost.auth_errors 0.0
servers.hostname.memcached.localhost.bytes 0.0
servers.hostname.memcached.localhost.bytes_read 0
servers.hostname.memcached.localhost.bytes_written 0.0
servers.hostname.memcached.localhost.cas_badval 0.0
servers.hostname.memcached.localhost.cas_hits 0.0
servers.hostname.memcached.localhost.cas_misses 0.0
servers.hostname.memcached.localhost.cmd_flush 0.0
servers.hostname.memcached.localhost.cmd_get 0.0
servers.hostname.memcached.localhost.cmd_set 0.0
servers.hostname.memcached.localhost.cmd_touch 0.0
servers.hostname.memcached.localhost.conn_yields 0.0
servers.hostname.memcached.localhost.connection_structures 11.0
servers.hostname.memcached.localhost.curr_connections 10.0
servers.hostname.memcached.localhost.curr_items 0.0
servers.hostname.memcached.localhost.decr_hits 0.0
servers.hostname.memcached.localhost.decr_misses 0.0
servers.hostname.memcached.localhost.delete_hits 0.0
servers.hostname.memcached.localhost.delete_misses 0.0
servers.hostname.memcached.localhost.evicted_unfetched 0.0
servers.hostname.memcached.localhost.evictions 0.0
servers.hostname.memcached.localhost.expired_unfetched 0.0
servers.hostname.memcached.localhost.get_hits 0.0
servers.hostname.memcached.localhost.get_misses 0.0
servers.hostname.memcached.localhost.hash_bytes 524288.0
servers.hostname.memcached.localhost.hash_is_expanding 0.0
servers.hostname.memcached.localhost.hash_power_level 16.0
servers.hostname.memcached.localhost.incr_hits 0.0
servers.hostname.memcached.localhost.incr_misses 0.0
servers.hostname.memcached.localhost.limit_maxbytes 67108864.0
servers.hostname.memcached.localhost.listen_disabled_num 0.0
servers.hostname.memcached.localhost.reclaimed 0.0
servers.hostname.memcached.localhost.repcached_qi_free 0.0
servers.hostname.memcached.localhost.reserved_fds 20.0
servers.hostname.memcached.localhost.rusage_system 0.195071
servers.hostname.memcached.localhost.rusage_user 0.231516
servers.hostname.memcached.localhost.threads 4.0
servers.hostname.memcached.localhost.total_connections 0
servers.hostname.memcached.localhost.total_items 0.0
servers.hostname.memcached.localhost.touch_hits 0.0
servers.hostname.memcached.localhost.touch_misses 0.0
servers.hostname.memcached.localhost.uptime 25763
```

