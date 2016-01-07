<!--This file was generated from the python source
Please edit the source to make changes
-->
ZookeeperCollector
=====

Collect zookeeper stats. ( Modified from memcached collector )

#### Dependencies

 * subprocess
 * Zookeeper 'mntr' command (zookeeper version => 3.4.0)

#### Example Configuration

ZookeeperCollector.conf

```
    enabled = True
    hosts = localhost:2181, app-1@localhost:2181, app-2@localhost:2181, etc
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
hosts | localhost:2181, | List of hosts, and ports to collect. Set an alias by  prefixing the host:port with alias@ | list
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
publish |  | Which rows of 'status' you would like to publish. Telnet host port' and type stats and hit enter to see the  list of possibilities. Leave unset to publish all. | 

#### Example Output

```
__EXAMPLESHERE__
```

