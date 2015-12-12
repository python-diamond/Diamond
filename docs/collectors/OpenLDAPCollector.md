<!--This file was generated from the python source
Please edit the source to make changes
-->
OpenLDAPCollector
=====

Collects data from a OpenLDAP server.

#### Dependencies

 * ldap module


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
host | localhost | Hostname to collect from | str
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
password | password | Password of user we connect with | str
port | 389 | Port number to collect from | int
username | cn=monitor | DN of user we connect with | str

#### Example Output

```
__EXAMPLESHERE__
```

