UPSCollector
=====

This class collects data from NUT, a UPS interface for linux.

#### Dependencies

 * nut/upsc to be installed, configured and running.


#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>bin</td><td>/bin/upsc</td><td>The path to the upsc binary</td><td>str</td></tr>
<tr><td>byte_unit</td><td>byte</td><td>Default numeric output(s)</td><td>str</td></tr>
<tr><td>enabled</td><td>False</td><td>Enable collecting these metrics</td><td>bool</td></tr>
<tr><td>measure_collector_time</td><td>False</td><td>Collect the collector run time in ms</td><td>bool</td></tr>
<tr><td>metrics_blacklist</td><td>None</td><td>Regex to match metrics to block. Mutually exclusive with metrics_whitelist</td><td>NoneType</td></tr>
<tr><td>metrics_whitelist</td><td>None</td><td>Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist</td><td>NoneType</td></tr>
<tr><td>sudo_cmd</td><td>/usr/bin/sudo</td><td>Path to sudo</td><td>str</td></tr>
<tr><td>ups_name</td><td>cyberpower</td><td>The name of the ups to collect data for</td><td>str</td></tr>
<tr><td>use_sudo</td><td>False</td><td>Use sudo?</td><td>bool</td></tr>
</table>

#### Example Output

```
servers.hostname.ups.battery.charge.charge 100.0
servers.hostname.ups.battery.charge.low 10.0
servers.hostname.ups.battery.charge.warning 20.0
servers.hostname.ups.battery.runtime.low 300.0
servers.hostname.ups.battery.runtime.runtime 960.0
servers.hostname.ups.battery.voltage.nominal 12.0
servers.hostname.ups.battery.voltage.voltage 4.9
servers.hostname.ups.driver.parameter.pollfreq 30.0
servers.hostname.ups.driver.parameter.pollinterval 2.0
servers.hostname.ups.driver.version.internal 0.34
servers.hostname.ups.input.transfer.high 0.0
servers.hostname.ups.input.transfer.low 0.0
servers.hostname.ups.input.voltage.nominal 120.0
servers.hostname.ups.input.voltage.voltage 121.0
servers.hostname.ups.output.voltage.voltage 120.0
servers.hostname.ups.ups.delay.shutdown 20.0
servers.hostname.ups.ups.delay.start 30.0
servers.hostname.ups.ups.load.load 46.0
servers.hostname.ups.ups.productid.productid 501.0
servers.hostname.ups.ups.realpower.nominal 330.0
servers.hostname.ups.ups.timer.shutdown -60.0
servers.hostname.ups.ups.timer.start 0.0
servers.hostname.ups.ups.vendorid.vendorid 764.0
```

### This file was generated from the python source
### Please edit the source to make changes

