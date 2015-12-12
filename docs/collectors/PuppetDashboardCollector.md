<!--This file was generated from the python source
Please edit the source to make changes
-->
PuppetDashboardCollector
=====

Collect metrics from Puppet Dashboard

#### Dependencies

 * urllib2


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
host | localhost | Hostname to collect from | str
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
path | puppetdashboard | Path to the dashboard | str
port | 5678 | Port number to collect from | int

#### Example Output

```
servers.hostname.puppetdashboard.changed 10
servers.hostname.puppetdashboard.pending 0
servers.hostname.puppetdashboard.unchanged 4
servers.hostname.puppetdashboard.unreported 0
servers.hostname.puppetdashboard.unresponsive 3
```

