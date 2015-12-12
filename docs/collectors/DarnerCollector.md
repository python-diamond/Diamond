<!--This file was generated from the python source
Please edit the source to make changes
-->
DarnerCollector
=====

Collect darner stats ( Modified from memcached collector )



#### Example Configuration

DarnerCollector.conf

```
    enabled = True
    hosts = localhost:22133, app-1@localhost:22133, app-2@localhost:22133, etc
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
hosts | localhost:22133, | List of hosts, and ports to collect. Set an alias by  prefixing the host:port with alias@ | list
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
publish |  | Which rows of 'status' you would like to publish. Telnet host port' and type stats and hit enter to see  the list of possibilities. Leave unset to publish all. | 
publish_queues | True | Publish queue stats (defaults to True) | bool

#### Example Output

```
servers.hostname.darner.localhost.cmd_get 100
servers.hostname.darner.localhost.cmd_set 150
servers.hostname.darner.localhost.curr_connections 2
servers.hostname.darner.localhost.queues.test1.items 2
servers.hostname.darner.localhost.queues.test1.open_transactions 8
servers.hostname.darner.localhost.queues.test1.waiters 4
servers.hostname.darner.localhost.queues.test_2.items 16
servers.hostname.darner.localhost.queues.test_2.open_transactions 64
servers.hostname.darner.localhost.queues.test_2.waiters 32
servers.hostname.darner.localhost.queues.test_3_bar.items 128
servers.hostname.darner.localhost.queues.test_3_bar.open_transactions 512
servers.hostname.darner.localhost.queues.test_3_bar.waiters 256
servers.hostname.darner.localhost.total_connections 15
servers.hostname.darner.localhost.total_items 20
servers.hostname.darner.localhost.uptime 2422175
```

