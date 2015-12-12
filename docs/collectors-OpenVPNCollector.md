OpenVPNCollector
=====

Processes OpenVPN metrics. This collector can process multiple OpenVPN
instances (even from a server box). In addition to the path, you may
also specify a name of the instance.

You can use both the status file or the tcp management connection to
retrieve the metrics.

To parse the status file::

    instances = file:///var/log/openvpn/status.log

Or, to override the name (now "status"):

    instances = file:///var/log/openvpn/status.log?developers

To use the management connection::

    instances = tcp://127.0.0.1:1195

Or, to override the name (now "127_0_0_1"):

    instances = tcp://127.0.0.1:1195?developers

You can also specify multiple and mixed instances::

    instances = file:///var/log/openvpn/openvpn.log, tcp://10.0.0.1:1195?admins

#### Dependencies

 * urlparse


#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>byte_unit</td><td>byte</td><td>Default numeric output(s)</td><td>str</td></tr>
<tr><td>enabled</td><td>False</td><td>Enable collecting these metrics</td><td>bool</td></tr>
<tr><td>instances</td><td>file:///var/log/openvpn/status.log</td><td>List of instances to collect stats from</td><td>str</td></tr>
<tr><td>measure_collector_time</td><td>False</td><td>Collect the collector run time in ms</td><td>bool</td></tr>
<tr><td>metrics_blacklist</td><td>None</td><td>Regex to match metrics to block. Mutually exclusive with metrics_whitelist</td><td>NoneType</td></tr>
<tr><td>metrics_whitelist</td><td>None</td><td>Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist</td><td>NoneType</td></tr>
<tr><td>timeout</td><td>10</td><td>network timeout</td><td>str</td></tr>
</table>

#### Example Output

```
servers.hostname.openvpn.status.clients.a_example_org.bytes_rx 109619579.0
servers.hostname.openvpn.status.clients.a_example_org.bytes_tx 935436488.0
servers.hostname.openvpn.status.clients.b_example_org.bytes_rx 25067295.0
servers.hostname.openvpn.status.clients.b_example_org.bytes_tx 10497532.0
servers.hostname.openvpn.status.clients.c_example_org.bytes_rx 21842093.0
servers.hostname.openvpn.status.clients.c_example_org.bytes_tx 20185134.0
servers.hostname.openvpn.status.clients.connected 5
servers.hostname.openvpn.status.clients.d_example_org.bytes_rx 4559242.0
servers.hostname.openvpn.status.clients.d_example_org.bytes_tx 11133831.0
servers.hostname.openvpn.status.clients.e_example_org.bytes_rx 13090090.0
servers.hostname.openvpn.status.clients.e_example_org.bytes_tx 13401853.0
servers.hostname.openvpn.status.global.max_bcast-mcast_queue_length 14.0
```

### This file was generated from the python source
### Please edit the source to make changes

