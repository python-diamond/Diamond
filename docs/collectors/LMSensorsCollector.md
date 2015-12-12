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


#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>byte_unit</td><td>byte</td><td>Default numeric output(s)</td><td>str</td></tr>
<tr><td>enabled</td><td>False</td><td>Enable collecting these metrics</td><td>bool</td></tr>
<tr><td>measure_collector_time</td><td>False</td><td>Collect the collector run time in ms</td><td>bool</td></tr>
<tr><td>metrics_blacklist</td><td>None</td><td>Regex to match metrics to block. Mutually exclusive with metrics_whitelist</td><td>NoneType</td></tr>
<tr><td>metrics_whitelist</td><td>None</td><td>Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist</td><td>NoneType</td></tr>
<tr><td>send_zero</td><td>False</td><td>Send sensor data even when there is no value</td><td>bool</td></tr>
</table>

#### Example Output

```
__EXAMPLESHERE__
```

### This file was generated from the python source
### Please edit the source to make changes

