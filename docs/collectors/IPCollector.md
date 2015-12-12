<!--This file was generated from the python source
Please edit the source to make changes
-->
IPCollector
=====

The IPCollector class collects metrics on IP stats

#### Dependencies

 * /proc/net/snmp

#### Allowed Metric Names
<table>
<tr><th>Name</th></tr>
<tr><th>InAddrErrors</th></tr>
<tr><th>InDelivers</th></tr>
<tr><th>InDiscards</th></tr>
<tr><th>InHdrErrors</th></tr>
<tr><th>InReceives</th></tr>
<tr><th>InUnknownProtos</th></tr>
<tr><th>OutDiscards</th></tr>
<tr><th>OutNoRoutes</th></tr>
<tr><th>OutRequests</th></tr>
</table>


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
allowed_names | InAddrErrors, InDelivers, InDiscards, InHdrErrors, InReceives, InUnknownProtos, OutDiscards, OutNoRoutes, OutRequests | list of entries to collect, empty to collect all | str
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType

#### Example Output

```
servers.hostname.ip.DefaultTTL 64
servers.hostname.ip.ForwDatagrams 0
servers.hostname.ip.Forwarding 2
servers.hostname.ip.FragCreates 0
servers.hostname.ip.FragFails 0
servers.hostname.ip.FragOKs 0
servers.hostname.ip.InAddrErrors 0
servers.hostname.ip.InDelivers 2
servers.hostname.ip.InDiscards 0
servers.hostname.ip.InHdrErrors 0
servers.hostname.ip.InReceives 2
servers.hostname.ip.InUnknownProtos 0
servers.hostname.ip.OutDiscards 0
servers.hostname.ip.OutNoRoutes 0
servers.hostname.ip.OutRequests 1
servers.hostname.ip.ReasmFails 0
servers.hostname.ip.ReasmOKs 0
servers.hostname.ip.ReasmReqds 0
servers.hostname.ip.ReasmTimeout 0
```

