<!--This file was generated from the python source
Please edit the source to make changes
-->
UsersCollector
=====

Collects the number of users logged in and shells per user

#### Dependencies

 * [pyutmp](http://software.clapper.org/pyutmp/)
or
 * [utmp] (python-utmp on Debian and derivatives)


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
servers.hostname.users.kormoc 2
servers.hostname.users.root 3
servers.hostname.users.total 5
```

