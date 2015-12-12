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



#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>auth</td><td>None</td><td>Password?</td><td>NoneType</td></tr>
<tr><td>byte_unit</td><td>byte</td><td>Default numeric output(s)</td><td>str</td></tr>
<tr><td>databases</td><td>16</td><td>how many database instances to collect</td><td>int</td></tr>
<tr><td>db</td><td>0</td><td></td><td>int</td></tr>
<tr><td>enabled</td><td>False</td><td>Enable collecting these metrics</td><td>bool</td></tr>
<tr><td>host</td><td>localhost</td><td>Hostname to collect from</td><td>str</td></tr>
<tr><td>instances</td><td>,</td><td>Redis addresses, comma separated, syntax: nick1@host:port, nick2@:port or nick3@host</td><td>list</td></tr>
<tr><td>measure_collector_time</td><td>False</td><td>Collect the collector run time in ms</td><td>bool</td></tr>
<tr><td>metrics_blacklist</td><td>None</td><td>Regex to match metrics to block. Mutually exclusive with metrics_whitelist</td><td>NoneType</td></tr>
<tr><td>metrics_whitelist</td><td>None</td><td>Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist</td><td>NoneType</td></tr>
<tr><td>port</td><td>6379</td><td>Port number to collect from</td><td>int</td></tr>
<tr><td>timeout</td><td>5</td><td>Socket timeout</td><td>int</td></tr>
</table>

#### Example Output

```
__EXAMPLESHERE__
```

### This file was generated from the python source
### Please edit the source to make changes

