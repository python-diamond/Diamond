<!--This file was generated from the python source
Please edit the source to make changes
-->
PowerDNSCollector
=====

Collects all metrics exported by the powerdns nameserver using the
pdns_control binary.

#### Dependencies

 * pdns_control


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
bin | /usr/bin/pdns_control | The path to the pdns_control binary | str
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
sudo_cmd | /usr/bin/sudo | Path to sudo | str
use_sudo | False | Use sudo? | bool

#### Example Output

```
servers.hostname.powerdns.corrupt-packets 1.0
servers.hostname.powerdns.deferred-cache-inserts 2.0
servers.hostname.powerdns.deferred-cache-lookup 3.0
servers.hostname.powerdns.latency 4.0
servers.hostname.powerdns.packetcache-hit 5.0
servers.hostname.powerdns.packetcache-miss 6.0
servers.hostname.powerdns.packetcache-size 7.0
servers.hostname.powerdns.qsize-q 8.0
servers.hostname.powerdns.query-cache-hit 9.0
servers.hostname.powerdns.query-cache-miss 10.0
servers.hostname.powerdns.recursing-answers 11.0
servers.hostname.powerdns.recursing-questions 12.0
servers.hostname.powerdns.servfail-packets 13.0
servers.hostname.powerdns.tcp-answers 14.0
servers.hostname.powerdns.tcp-queries 15.0
servers.hostname.powerdns.timedout-packets 16.0
servers.hostname.powerdns.udp-answers 17.0
servers.hostname.powerdns.udp-queries 18.0
servers.hostname.powerdns.udp4-answers 19.0
servers.hostname.powerdns.udp4-queries 20.0
servers.hostname.powerdns.udp6-answers 21.0
servers.hostname.powerdns.udp6-queries 22.0
```

