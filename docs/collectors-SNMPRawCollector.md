SNMPRawCollector
=====

The SNMPRawCollector is designed for collecting data from SNMP-enables devices,
using a set of specified OIDs

#### Configuration

Below is an example configuration for the SNMPRawCollector. The collector
can collect data any number of devices by adding configuration sections
under the *devices* header. By default the collector will collect every 60
seconds. This might be a bit excessive and put unnecessary load on the
devices being polled. You may wish to change this to every 300 seconds. However
you need modify your graphite data retentions to handle this properly.

```
    # Options for SNMPRawCollector
    enabled = True
    interval = 60

    [devices]

    # Start the device configuration
    # Note: this name will be used in the metric path.
    [[my-identification-for-this-host]]
    host = localhost
    port = 161
    community = public

    # Start the OID list for this device
    # Note: the value part will be used in the metric path.
    [[[oids]]]
    1.3.6.1.4.1.2021.10.1.3.1 = cpu.load.1min
    1.3.6.1.4.1.2021.10.1.3.2 = cpu.load.5min
    1.3.6.1.4.1.2021.10.1.3.3 = cpu.load.15min

    # If you want another host, you can. But you probably won't need it.
    [[another-identification]]
    host = router1.example.com
    port = 161
    community = public
    [[[oids]]]
    oid = metric.path
    oid = metric.path
```

Note: If you modify the SNMPRawCollector configuration, you will need to
restart diamond.

#### Dependencies

 * pysmnp (which depends on pyasn1 0.1.7 and pycrypto)


#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>byte_unit</td><td>byte</td><td>Default numeric output(s)</td><td>str</td></tr>
<tr><td>enabled</td><td>False</td><td>Enable collecting these metrics</td><td>bool</td></tr>
<tr><td>measure_collector_time</td><td>False</td><td>Collect the collector run time in ms</td><td>bool</td></tr>
<tr><td>metrics_blacklist</td><td>None</td><td>Regex to match metrics to block. Mutually exclusive with metrics_whitelist</td><td>NoneType</td></tr>
<tr><td>metrics_whitelist</td><td>None</td><td>Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist</td><td>NoneType</td></tr>
<tr><td>retries</td><td>3</td><td>Number of times to retry before bailing</td><td>int</td></tr>
<tr><td>timeout</td><td>5</td><td>Seconds before timing out the snmp connection</td><td>int</td></tr>
</table>

#### Example Output

```
__EXAMPLESHERE__
```

### This file was generated from the python source
### Please edit the source to make changes

