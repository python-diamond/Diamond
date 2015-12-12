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

#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>byte_unit</td><td>byte</td><td>Default numeric output(s)</td><td>str</td></tr>
<tr><td>enabled</td><td>False</td><td>Enable collecting these metrics</td><td>bool</td></tr>
<tr><td>hosts</td><td>localhost:22133,</td><td>List of hosts, and ports to collect. Set an alias by  prefixing the host:port with alias@</td><td>list</td></tr>
<tr><td>measure_collector_time</td><td>False</td><td>Collect the collector run time in ms</td><td>bool</td></tr>
<tr><td>metrics_blacklist</td><td>None</td><td>Regex to match metrics to block. Mutually exclusive with metrics_whitelist</td><td>NoneType</td></tr>
<tr><td>metrics_whitelist</td><td>None</td><td>Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist</td><td>NoneType</td></tr>
<tr><td>publish</td><td></td><td>Which rows of 'status' you would like to publish. Telnet host port' and type stats and hit enter to see  the list of possibilities. Leave unset to publish all.</td><td></td></tr>
<tr><td>publish_queues</td><td>True</td><td>Publish queue stats (defaults to True)</td><td>bool</td></tr>
</table>

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

### This file was generated from the python source
### Please edit the source to make changes

