<!--This file was generated from the python source
Please edit the source to make changes
-->
SNMPInterfaceCollector
=====

The SNMPInterfaceCollector is designed for collecting interface data from
remote SNMP-enabled devices such as routers and switches using SNMP IF_MIB

#### Installation

The snmpinterfacecollector.py module should be installed into your Diamond
installation collectors directory. This directory is defined
in diamond.cfg under the *collectors_path* directive. This defaults to
*/usr/lib/diamond/collectors/* on Ubuntu.

The SNMPInterfaceCollector.cfg file should be installed into your diamond
installation config directory. This directory is defined
in diamond.cfg under the *collectors_config_path* directive. This defaults to
*/etc/diamond/* on Ubuntu.

Once the collector is installed and configured, you can wait for diamond to
pick up the new collector automatically, or simply restart diamond.

#### Configuration

Below is an example configuration for the SNMPInterfaceCollector. The collector
can collect data any number of devices by adding configuration sections
under the *devices* header. By default the collector will collect every 60
seconds. This might be a bit excessive and put unnecessary load on the
devices being polled. You may wish to change this to every 300 seconds. However
you need modify your graphite data retentions to handle this properly.

```
    # Options for SNMPInterfaceCollector
    path = interface
    interval = 60

    [devices]

    [[router1]]
    host = router1.example.com
    port = 161
    community = public

    [[router2]]
    host = router1.example.com
    port = 161
    community = public
```

Note: If you modify the SNMPInterfaceCollector configuration, you will need to
restart diamond.

#### Dependencies

 * pysmnp

#### Notes

This implimentation is well suited for collecting a small number of metrics
locally. If you want to collect a large number of remote metrics, consider
https://github.com/GreggBzz/snmp-interface-poll as an alternative collector


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | bit, byte, | Default numeric output(s) | list
enabled | False | Enable collecting these metrics | bool
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
retries | 3 | Number of times to retry before bailing | int
timeout | 5 | Seconds before timing out the snmp connection | int

#### Example Output

```
__EXAMPLESHERE__
```

