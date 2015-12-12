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


#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>byte_unit</td><td>byte</td><td>Default numeric output(s)</td><td>str</td></tr>
<tr><td>enabled</td><td>False</td><td>Enable collecting these metrics</td><td>bool</td></tr>
<tr><td>measure_collector_time</td><td>False</td><td>Collect the collector run time in ms</td><td>bool</td></tr>
<tr><td>metrics_blacklist</td><td>None</td><td>Regex to match metrics to block. Mutually exclusive with metrics_whitelist</td><td>NoneType</td></tr>
<tr><td>metrics_whitelist</td><td>None</td><td>Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist</td><td>NoneType</td></tr>
<tr><td>xmlrpc_server_path</td><td>/var/run/supervisor.sock</td><td>XML-RPC server path.</td><td>str</td></tr>
<tr><td>xmlrpc_server_protocol</td><td>unix</td><td>XML-RPC server protocol. Options: unix, http</td><td>str</td></tr>
</table>

#### Example Output

```
servers.hostname.supervisor.test_group.test_name_1.state 20
servers.hostname.supervisor.test_group.test_name_1.uptime 5
servers.hostname.supervisor.test_group.test_name_2.state 200
servers.hostname.supervisor.test_group.test_name_2.uptime 500
```

### This file was generated from the python source
### Please edit the source to make changes

