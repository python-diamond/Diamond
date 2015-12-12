PingCollector
=====

Collect icmp round trip times
Only valid for ipv4 hosts currently

#### Dependencies

 * ping

#### Configuration

Configuration is done by:

Create a file named: PingCollector.conf in the collectors_config_path

 * enabled = true
 * interval = 60
 * target_1 = example.org
 * target_fw = 192.168.0.1
 * target_localhost = localhost

Test your configuration using the following command:

diamond-setup --print -C PingCollector

You should get a response back that indicates 'enabled': True and see entries
for your targets in pairs like:

'target_1': 'example.org'

We extract out the key after target_ and use it in the graphite node we push.


#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>bin</td><td>/bin/ping</td><td>The path to the ping binary</td><td>str</td></tr>
<tr><td>byte_unit</td><td>byte</td><td>Default numeric output(s)</td><td>str</td></tr>
<tr><td>enabled</td><td>False</td><td>Enable collecting these metrics</td><td>bool</td></tr>
<tr><td>measure_collector_time</td><td>False</td><td>Collect the collector run time in ms</td><td>bool</td></tr>
<tr><td>metrics_blacklist</td><td>None</td><td>Regex to match metrics to block. Mutually exclusive with metrics_whitelist</td><td>NoneType</td></tr>
<tr><td>metrics_whitelist</td><td>None</td><td>Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist</td><td>NoneType</td></tr>
<tr><td>sudo_cmd</td><td>/usr/bin/sudo</td><td>Path to sudo</td><td>str</td></tr>
<tr><td>use_sudo</td><td>False</td><td>Use sudo?</td><td>bool</td></tr>
</table>

#### Example Output

```
__EXAMPLESHERE__
```

### This file was generated from the python source
### Please edit the source to make changes

