<!--This file was generated from the python source
Please edit the source to make changes
-->
UPSCollector
=====

This class collects data from NUT, a UPS interface for linux.

#### Dependencies

 * nut/upsc to be installed, configured and running.


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
bin | /bin/upsc | The path to the upsc binary | str
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
sudo_cmd | /usr/bin/sudo | Path to sudo | str
ups_name | cyberpower | The name of the ups to collect data for | str
use_sudo | False | Use sudo? | bool

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

