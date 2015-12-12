<!--This file was generated from the python source
Please edit the source to make changes
-->
LMSensorsCollector
=====

This class collects data from libsensors. It should work against libsensors 2.x
and 3.x, pending support within the PySensors Ctypes binding:
[http://pypi.python.org/pypi/PySensors/](http://pypi.python.org/pypi/PySensors/)

Requires: 'sensors' to be installed, configured, and the relevant kernel
modules to be loaded. Requires: PySensors requires Python 2.6+

If you're having issues, check your version of 'sensors'. This collector
written against: sensors version 3.1.2 with libsensors version 3.1.2

#### Dependencies

 * [PySensors](http://pypi.python.org/pypi/PySensors/)


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
send_zero | False | Send sensor data even when there is no value | bool

#### Example Output

```
__EXAMPLESHERE__
```

