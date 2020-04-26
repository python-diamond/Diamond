<!--This file was generated from the python source
Please edit the source to make changes
-->
OneWireCollector
=====

The OneWireCollector collects data from 1-Wire Filesystem

You can configure which sensors are read in two way:

-  add section [scan] with attributes and aliases,
   (collector will scan owfs to find attributes)

or

- add sections with format id:$SENSOR_ID

See also: http://owfs.org/
Author: Tomasz Prus

#### Dependencies

 * owfs


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType

#### Example Output

```
servers.hostname.owfs.28_2F702A010000.p11 999
servers.hostname.owfs.28_A76569020000.t 22.4375
```

