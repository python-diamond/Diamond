<!--This file was generated from the python source
Please edit the source to make changes
-->
RedisCollector
=====

Collects data from one or more Redis Servers

#### Dependencies

 * redis

#### Notes

The collector is named an odd redisstat because of an import issue with
having the python library called redis and this collector's module being called
redis, so we use an odd name for this collector. This doesn't affect the usage
of this collector.

Example config file RedisCollector.conf

```
enabled=True
host=redis.example.com
port=16379
auth=PASSWORD
```

or for multi-instance mode:

```
enabled=True
instances = nick1@host1:port1, nick2@host2:port2/PASSWORD, ...
```

For connecting via unix sockets, provide the path prefixed with ``unix:``
instead of the host, e.g.

```
enabled=True
host=unix:/var/run/redis/redis.sock
```

or

```
enabled = True
instances = nick3@unix:/var/run/redis.sock:/PASSWORD
```

In that case, for disambiguation there must be a colon ``:`` before the slash
``/`` followed by the password.

Note: when using the host/port config mode, the port number is used in
the metric key. When using the multi-instance mode, the nick will be used.
If not specified the port will be used. In case of unix sockets, the base name
without file extension (i.e. in the aforementioned examples ``redis``)
is the default metric key.



#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
auth | None | Password? | NoneType
byte_unit | byte | Default numeric output(s) | str
databases | 16 | how many database instances to collect | int
db | 0 |  | int
enabled | False | Enable collecting these metrics | bool
host | localhost | Hostname to collect from | str
instances | , | Redis addresses, comma separated, syntax: nick1@host:port, nick2@:port or nick3@host | list
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
port | 6379 | Port number to collect from | int
timeout | 5 | Socket timeout | int

#### Example Output

```
__EXAMPLESHERE__
```

