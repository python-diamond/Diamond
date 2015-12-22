<!--This file was generated from the python source
Please edit the source to make changes
-->
IPMISensorCollector
=====

This collector uses the [ipmitool](http://openipmi.sourceforge.net/) to read
hardware sensors from servers
using the Intelligent Platform Management Interface (IPMI). IPMI is very common
with server hardware but usually not available in consumer hardware.

#### Dependencies

 * [ipmitool](http://openipmi.sourceforge.net/)


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
bin | /usr/bin/ipmitool | Path to the ipmitool binary | str
byte_unit | byte | Default numeric output(s) | str
delimiter | . | Parse blanks in sensor names into a delimiter | str
enabled | False | Enable collecting these metrics | bool
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
sudo_cmd | /usr/bin/sudo | Path to sudo | str
thresholds | False | Collect thresholds as well as reading | bool
use_sudo | False | Use sudo? | bool

#### Example Output

```
servers.hostname.ipmi.sensors.+12V 12.031
servers.hostname.ipmi.sensors.+1_1V 1.112
servers.hostname.ipmi.sensors.+1_5V 1.512
servers.hostname.ipmi.sensors.+1_8V 1.824
servers.hostname.ipmi.sensors.+3_3V 3.288
servers.hostname.ipmi.sensors.+3_3VSB 3.24
servers.hostname.ipmi.sensors.+5V 4.992
servers.hostname.ipmi.sensors.CPU1.DIMM 1.512
servers.hostname.ipmi.sensors.CPU1.Temp 0.0
servers.hostname.ipmi.sensors.CPU1.VTT 1.12
servers.hostname.ipmi.sensors.CPU1.Vcore 1.08
servers.hostname.ipmi.sensors.CPU2.DIMM 1.512
servers.hostname.ipmi.sensors.CPU2.Temp 0.0
servers.hostname.ipmi.sensors.CPU2.VTT 1.176
servers.hostname.ipmi.sensors.CPU2.Vcore 1.0
servers.hostname.ipmi.sensors.Fan1 4185.0
servers.hostname.ipmi.sensors.Fan2 4185.0
servers.hostname.ipmi.sensors.Fan3 4185.0
servers.hostname.ipmi.sensors.Fan7 3915.0
servers.hostname.ipmi.sensors.Fan8 3915.0
servers.hostname.ipmi.sensors.Intrusion 0.0
servers.hostname.ipmi.sensors.P1-DIMM1A.Temp 41.0
servers.hostname.ipmi.sensors.P1-DIMM1B.Temp 39.0
servers.hostname.ipmi.sensors.P1-DIMM2A.Temp 38.0
servers.hostname.ipmi.sensors.P1-DIMM2B.Temp 40.0
servers.hostname.ipmi.sensors.P1-DIMM3A.Temp 37.0
servers.hostname.ipmi.sensors.P1-DIMM3B.Temp 38.0
servers.hostname.ipmi.sensors.P2-DIMM1A.Temp 39.0
servers.hostname.ipmi.sensors.P2-DIMM1B.Temp 38.0
servers.hostname.ipmi.sensors.P2-DIMM2A.Temp 39.0
servers.hostname.ipmi.sensors.P2-DIMM2B.Temp 39.0
servers.hostname.ipmi.sensors.P2-DIMM3A.Temp 39.0
servers.hostname.ipmi.sensors.P2-DIMM3B.Temp 40.0
servers.hostname.ipmi.sensors.PS.Status 0.0
servers.hostname.ipmi.sensors.System.Temp 32.0
servers.hostname.ipmi.sensors.VBAT 3.24
```

