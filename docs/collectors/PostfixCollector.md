<!--This file was generated from the python source
Please edit the source to make changes
-->
PostfixCollector
=====

Collect stats from postfix-stats. postfix-stats is a simple threaded stats
aggregator for Postfix. When running as a syslog destination, it can be used to
get realtime cumulative stats.

#### Dependencies

 * socket
 * json (or simplejson)
 * [postfix-stats](https://github.com/disqus/postfix-stats)


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
host | localhost | Hostname to connect to | str
include_clients | True | Include client connection stats | bool
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
port | 7777 | Port to connect to | int

#### Example Output

```
servers.hostname.postfix.clients.127_0_0_1 1
servers.hostname.postfix.send.resp_codes.2_0_0 5
servers.hostname.postfix.send.status.sent 4
```

