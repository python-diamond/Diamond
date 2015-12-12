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


#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>byte_unit</td><td>byte</td><td>Default numeric output(s)</td><td>str</td></tr>
<tr><td>enabled</td><td>False</td><td>Enable collecting these metrics</td><td>bool</td></tr>
<tr><td>measure_collector_time</td><td>False</td><td>Collect the collector run time in ms</td><td>bool</td></tr>
<tr><td>metrics_blacklist</td><td>None</td><td>Regex to match metrics to block. Mutually exclusive with metrics_whitelist</td><td>NoneType</td></tr>
<tr><td>metrics_whitelist</td><td>None</td><td>Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist</td><td>NoneType</td></tr>
</table>

#### Example Output

```
__EXAMPLESHERE__
```

### This file was generated from the python source
### Please edit the source to make changes

