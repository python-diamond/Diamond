<!--This file was generated from the python source
Please edit the source to make changes
-->
UDPCollector
=====

The UDPCollector class collects metrics on UDP stats (surprise!)

#### Dependencies

 * /proc/net/snmp


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
allowed_names | InDatagrams, NoPorts, InErrors, OutDatagrams, RcvbufErrors, SndbufErrors | list of entries to collect, empty to collect all | str
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType

#### Example Output

```
servers.hostname.udp.InDatagrams 352320636.0
servers.hostname.udp.InErrors 5.0
servers.hostname.udp.NoPorts 449.0
servers.hostname.udp.OutDatagrams 352353358.0
```

