<!--This file was generated from the python source
Please edit the source to make changes
-->
NetworkCollector
=====

The NetworkCollector class collects metrics on network interface usage
using /proc/net/dev.

#### Dependencies

 * /proc/net/dev


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | bit, byte, | Default numeric output(s) | list
enabled | False | Enable collecting these metrics | bool
greedy | true | Greedy match interfaces | str
interfaces | eth, bond, em, p1p, eno, enp, ens, enx, | List of interface types to collect | list
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType

#### Example Output

```
servers.hostname.network.bond3.rx_megabyte (2.504, 2)
servers.hostname.network.bond3.tx_megabyte (4.707, 2)
servers.hostname.network.em2.rx_megabyte (2.504, 2)
servers.hostname.network.em2.tx_megabyte (4.707, 2)
servers.hostname.network.eth0.rx_megabyte (2.504, 2)
servers.hostname.network.eth0.tx_megabyte (4.707, 2)
servers.hostname.network.eth1.rx_megabyte (0.0, 2)
servers.hostname.network.eth1.tx_megabyte (0.0, 2)
```

