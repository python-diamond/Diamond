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

#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>byte_unit</td><td>byte</td><td>Default numeric output(s)</td><td>str</td></tr>
<tr><td>enabled</td><td>False</td><td>Enable collecting these metrics</td><td>bool</td></tr>
<tr><td>hosts</td><td>localhost:22222,</td><td>List of hosts, and ports to collect. Set an alias by  prefixing the host:port with alias@</td><td>list</td></tr>
<tr><td>measure_collector_time</td><td>False</td><td>Collect the collector run time in ms</td><td>bool</td></tr>
<tr><td>metrics_blacklist</td><td>None</td><td>Regex to match metrics to block. Mutually exclusive with metrics_whitelist</td><td>NoneType</td></tr>
<tr><td>metrics_whitelist</td><td>None</td><td>Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist</td><td>NoneType</td></tr>
</table>

#### Example Output

```
__EXAMPLESHERE__
```

### This file was generated from the python source
### Please edit the source to make changes

