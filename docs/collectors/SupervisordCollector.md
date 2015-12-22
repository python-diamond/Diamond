<!--This file was generated from the python source
Please edit the source to make changes
-->
SupervisordCollector
=====

Custom collector for supervisord process control system
(github.com/Supervisor/supervisor)

Supervisor runs an XML-RPC server, which this collector uses to gather a few
basic stats on each registered process.

#### Dependencies

 * xmlrpclib
 * supervisor
 * diamond

#### Usage

Configure supervisor's XML-RPC server (either over HTTP or Unix socket). See
supervisord.org/configuration.html for details. In the collector configuration
file, you may specify the protocol and path configuration; below are the
defaults.

<pre>
xmlrpc_server_protocol = unix
xmlrpc_server_path = /var/run/supervisor.sock
</pre>


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
xmlrpc_server_path | /var/run/supervisor.sock | XML-RPC server path. | str
xmlrpc_server_protocol | unix | XML-RPC server protocol. Options: unix, http | str

#### Example Output

```
servers.hostname.supervisor.test_group.test_name_1.state 20
servers.hostname.supervisor.test_group.test_name_1.uptime 5
servers.hostname.supervisor.test_group.test_name_2.state 200
servers.hostname.supervisor.test_group.test_name_2.uptime 500
```

