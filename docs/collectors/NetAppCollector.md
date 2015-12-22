<!--This file was generated from the python source
Please edit the source to make changes
-->
NetAppCollector
=====

The NetAppCollector collects metric from a NetApp installation using the
NetApp Manageability SDK. This allows access to many metrics not available
via SNMP.

For this to work you'll the SDK available on the system.
This module has been developed using v5.0 of the SDK.
As of writing the SDK can be found at
https://communities.netapp.com/docs/DOC-1152

You'll also need to specify which NetApp instances the collector should
get data from.

Example NetAppCollector.conf:
```
    enabled = True
    path_prefix = netapp

    [devices]

    [[na_filer]]
    ip = 123.123.123.123
    user = root
    password = strongpassword

````

The primary source for documentation about the API has been
"NetApp unified storage performance management using open interfaces"
https://communities.netapp.com/docs/DOC-1044


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
__EXAMPLESHERE__
```

